from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kb_backend.routers import members, chats

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(members.router, prefix="/members", tags=["members"])
app.include_router(chats.router, prefix="/chats", tags=["chats"])
