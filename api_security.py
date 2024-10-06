from enum import Enum
from http.client import UNAUTHORIZED
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from common import getenv

import logging
import os

load_dotenv()

env_auth_token = getenv('SS_AUTH_TOKEN').lower()

class AuthStatus(Enum):
    DISABLED = -1
    AUTHORIZED = 0
    UNAUTHORIZED = 1
    MISSING = 2

def is_authorized(req: Request):
    if len(env_auth_token) == 0:
        logging.info('SS_AUTH_TOKEN not set, authorization disabled')
        return AuthStatus.DISABLED

    bearer_token = req.headers.get('X-NWN-TOKEN')

    if bearer_token is None:
        return AuthStatus.MISSING
    if len(bearer_token) == 0:
        return AuthStatus.MISSING

    if bearer_token.lower() != env_auth_token:
        return AuthStatus.UNAUTHORIZED

    return AuthStatus.AUTHORIZED

def handle_auth_status(auth_status):
    if auth_status != AuthStatus.DISABLED:
        if auth_status == AuthStatus.UNAUTHORIZED:
            raise HTTPException(status_code=401) # unauthorized
        if auth_status == AuthStatus.MISSING:
            raise HTTPException(status_code=400) # bad request

def handle_authorization(req: Request):
    status = is_authorized(req)
    handle_auth_status(status)
