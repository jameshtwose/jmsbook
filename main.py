from typing import Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv
import os
import time
import models, schemas, utils
from database import engine, get_db
from routers import post, user, auth


#%%
# import os
# os.getcwd()
#%%

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

origins = [
    "http://127.0.0.1:5500/docs/index.html",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")

load_dotenv(find_dotenv())


while True:
    try:
        # Connect to an existing database
        conn = psycopg2.connect(host=os.getenv("cockroack_db_deta_host"), 
                                database=os.getenv("cockroack_db_deta_db"), 
                                user=os.getenv("cockroack_db_deta_user"),
                                password=os.getenv("cockroack_db_deta_pass"),
                                port=os.getenv("cockroack_db_deta_port"),
                                cursor_factory=RealDictCursor)
        # conn = psycopg2.connect(os.getenv("cockroack_db_deta_connect_string"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connection to database failed!")
        print(f"Error: {error}")
        time.sleep(2)

# file_path = "static/index.html"
# @app.get("/", response_class=FileResponse)
# def read_root():
#     return file_path

@app.get("/")
def read_root():
    return {"message": "welcome to my API"}




