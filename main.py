from fastapi import FastAPI
import uvicorn
from src.routes import notes, tags, contacts, auth, users
from src import settings
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


origins = [
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(notes.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "My 13 homework on WEB module"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
