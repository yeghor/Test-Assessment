from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import traveling
from database import initialize_models, get_engine, Base

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    engine = await get_engine()
    print("Initializing models")
    await initialize_models(engine=engine, Base=Base)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(traveling)

# Some frontend application or Nginx
origins = ["http://localhost:3000", "http://localhost:80"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
