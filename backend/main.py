from fastapi import FastAPI
from msgpack_asgi import MessagePackMiddleware

from endpoints.v1 import weather_consumer, base

app = FastAPI()
app.add_middleware(MessagePackMiddleware)

app.router.include_router(base.router, prefix='/api/v1')
app.router.include_router(weather_consumer.router, prefix='/api/v1')
