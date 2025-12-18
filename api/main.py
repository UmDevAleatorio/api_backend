from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import auth_router, order_router, product_router, user_router
from .database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Construction Store API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(order_router, prefix="/orders", tags=["Orders"])

@app.get("/")
def read_root():
    return {"message": "Construction Store API is running!"}