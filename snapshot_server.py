from fastapi import FastAPI, HTTPException, Request
from fastapi.datastructures import Default
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from api_models import ResponseModel, ProcessFileModel, DefaultResponses
from api_security import handle_authorization, AuthStatus
from common import getenv, ensure_directory

import os
import sys
import glob
import time
import logging
import shutil
import uvicorn

sys.path.insert(0, os.path.abspath('.'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

api = FastAPI()
api_cors_origins = [i for i in getenv('SS_API_CORS', '*').split(' ')]
api.add_middleware(CORSMiddleware, allow_origins=api_cors_origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

env_tmpdir = getenv('SS_TMPDIR')
env_dst_dir = getenv('SS_DSTDIR')
env_api_host = getenv('SS_API_HOST', '0.0.0.0')
env_api_port = int(getenv('SS_API_PORT', '8000'))

#################################################################

@api.get('/')
async def root() -> ResponseModel:
    return DefaultResponses.success

@api.get('/authtest')
async def authtest(request: Request) -> ResponseModel:
    handle_authorization(request)
    return DefaultResponses.success

@api.post('/api/v1/snapshot/processfile')
async def api_processfile(op: ProcessFileModel, request: Request):
    logger.info(f'api_processfile() called')

    handle_authorization(request)
        
    src_file = f'{env_tmpdir}/{op.filename}'
    dst_dir = f'{env_dst_dir}/{op.network}'
    dst_file = f'{dst_dir}/{op.filename}'

    ensure_directory(dst_dir)

    old_files = glob.glob(f'{dst_dir}/*')
    for f in old_files:
        logger.info(f'Removing old snapshot {f}')
        os.remove(f)

    logger.info(f'Moving new snapshot {src_file} to {dst_file}')
    shutil.move(src_file, dst_file)

    logger.info(f'File {op.filename} processed successfully')

    return {'status': 'success', 'message': f'File {op.filename} processed successfully'}


if __name__ == "__main__":
    uvicorn.run(api, host=env_api_host, port=env_api_port)