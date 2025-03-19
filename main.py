import json
from fastapi import FastAPI, HTTPException
from sentence_transformers import SentenceTransformer, util
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import routes
from contextlib import asynccontextmanager
from redis import Redis
import httpx

origins = [
    "http://localhost",
    "http://localhost:8080",
]

@asynccontextmanager
async def lifespan(router: FastAPI):
    try:
        routes.router.state.redis = Redis(host="3.15.60.69", port=6379, db=0)
        routes.router.state.client = httpx.AsyncClient()
        yield
        router.state.redis.close()
    except Exception as e:
        print(e)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount('/api', routes.router)

# documents = []

# model = SentenceTransformer("all-MiniLM-L6-v2")
# embedded_docs = {
#     doc["id"]: model.encode(doc['text'],convert_to_tensor=True) for doc in documents
# }

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)