from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging

from app.api.routers import api_router
from app.core.config import settings
from app.db.database import engine, Base
from app.db import seed
from app.services.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO)

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup Phase 
    Base.metadata.create_all(bind=engine)
    seed.init_db(engine)
    start_scheduler()
    yield
    # Teardown Phase
    stop_scheduler()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan
)

# Set up Rate Limiter at the Root
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")