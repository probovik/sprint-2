import json
import logging
import os
import time
from typing import List, Optional

import motor.motor_asyncio
from bson import ObjectId
from fastapi import Body, FastAPI, HTTPException, status
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from logmiddleware import RouterLoggingMiddleware, logging_config
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import BeforeValidator
from pymongo import errors
from typing_extensions import Annotated
from rediscluster import RedisCluster

# Configure JSON logging
logging.config.dictConfig(logging_config)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    RouterLoggingMiddleware,
    logger=logger,
)

DATABASE_URL = os.environ["MONGODB_URL"]
DATABASE_NAME = os.environ["MONGODB_DATABASE_NAME"]
REDIS_URLS = os.getenv("REDIS_URL", None).split(',')

def nocache(*args, **kwargs):
    def decorator(func):
        return func

    return decorator

if REDIS_URLS:
    cache = cache
else:
    cache = nocache

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

startup_nodes = [{"host": url.split('//')[1].split(':')[0], "port": url.split(':')[2]} for url in REDIS_URLS]

@app.on_event("startup")
async def startup():
    if REDIS_URLS:
        redis = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="api:cache")