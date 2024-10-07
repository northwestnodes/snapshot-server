from fastapi import FastAPI, HTTPException, Request
from fastapi.datastructures import Default
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from api_models import ResponseModel, ProcessFileModel, DefaultResponses
from api_security import handle_authorization, AuthStatus
from common import check_file, getenv, check_directory, remove_files, move_file

import os
import sys
import time
import logging
#import shutil
import uvicorn

sys.path.insert(0, os.path.abspath('.'))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(f'     snapshot_server')

load_dotenv()

api = FastAPI()
api_cors_origins = [i for i in getenv('SS_API_CORS', '*').split(' ')]
api.add_middleware(CORSMiddleware, allow_origins=api_cors_origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])

env_tmpdir = getenv('SS_TMPDIR')
env_dstdir = getenv('SS_DSTDIR')
env_api_host = getenv('SS_API_HOST', '0.0.0.0')
env_api_port = int(getenv('SS_API_PORT', '8000'))
env_api_timeout = int(getenv('SS_API_TIMEOUT', '3600'))

#################################################################

@api.get('/')
async def api_root() -> ResponseModel:
    return DefaultResponses.success

@api.post('/api/v1/snapshot/processfile')
async def api_processfile(op: ProcessFileModel, request: Request):
    handle_authorization(request)
        
    src_file = f'{env_tmpdir}/{op.filename}'
    dst_dir = f'{env_dstdir}/{op.network}'
    dst_file = f'{dst_dir}/{op.filename}'

    logger.info(f'Checking if {src_file} exists')
    check_file(src_file)

    logger.info(f'Checking if {dst_dir} exists')
    check_directory(dst_dir)

    logger.info(f'Removing old snapshot files from {dst_dir}')
    remove_files(dst_dir)

    logger.info(f'Moving {src_file} to {dst_file}')
    move_file(src_file, dst_file)

    logger.info(f'Snapshot successfully stored at {dst_file}')
    return DefaultResponses.success


if __name__ == '__main__':
    uvicorn.run(api, host=env_api_host, port=env_api_port, timeout_keep_alive=env_api_timeout)