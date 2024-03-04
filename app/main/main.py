from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.service.helper.environment import is_dev

load_dotenv()


app = FastAPI(
    title="FastApi",
    version="1.0.0",
)

if is_dev():
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://localhost:8100",
        "http://localhost:4200",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

from app.main.routes import *
