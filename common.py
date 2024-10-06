from fastapi import HTTPException

import os
import glob

def getenv(key, defaultValue=''):
    value = os.getenv(key)
    if value is None:
        return defaultValue
    if len(value) == 0:
        return defaultValue
    return value

def check_directory(path):
    os.makedirs(path, exist_ok=True)

def check_file(path):
    if not os.path.exists(path):
        raise HTTPException(status_code=503,detail=f'File not found: {path}')

def remove_files(path):
    old_files = glob.glob(f'{path}/*')
    for f in old_files:
        os.remove(f)