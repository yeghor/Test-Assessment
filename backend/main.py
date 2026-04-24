from fastapi import FastAPI
from routers import traveling

app = FastAPI()

app.include_router(traveling)

engine = None
