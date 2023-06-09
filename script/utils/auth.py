# auth.py

from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
import os
from dotenv import load_dotenv
load_dotenv()

api_key_header = APIKeyHeader(name="access_token", auto_error=False)

api_key_server = os.getenv["API_KEY"] # type: ignore


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == api_key_server:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
