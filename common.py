import os

def getenv(key, defaultValue=''):
    value = os.getenv(key)
    if value is None:
        return defaultValue
    if len(value) == 0:
        return defaultValue
    return value

def ensure_directory(path):
    os.makedirs(path, exist_ok=True)