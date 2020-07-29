import uvicorn
from fastapi import FastAPI
from msgpack_asgi import MessagePackMiddleware
import logging
from endpoints.v1 import weather_consumer, base
from logging import DEBUG

from fastapi.logger import logger
# ... other imports
import logging

gunicorn_logger = logging.getLogger('gunicorn.error')
logger.handlers = gunicorn_logger.handlers
if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(logging.DEBUG)
app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
app.add_middleware(MessagePackMiddleware)
app.router.include_router(base.router, prefix='/api/v1')
app.router.include_router(weather_consumer.router, prefix='/api/v1')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, log_level='debug', debug=True)
