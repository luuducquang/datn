import socketio
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode='asgi',cors_allowed_origins="*")

sio_app = socketio.ASGIApp(sio)

