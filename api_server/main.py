
from fastapi import FastAPI
from .handlers import router

app = FastAPI()

app.include_router(router)
