from fastapi import FastAPI
from .routers import tables_crud, user_crud, login


app = FastAPI()

"""Setting up middleware for CORS policy"""
from fastapi.middleware.cors import CORSMiddleware

origins = [
    # "https://www.google.co.in",
    # "https://www.google.com",
    # "*" #This is a wild card means all the websites can make request to my api.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(user_crud.router)
app.include_router(tables_crud.router)
