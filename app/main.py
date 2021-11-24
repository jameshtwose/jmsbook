from typing import Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv
import os
import time
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

load_dotenv(find_dotenv())


while True:
    try:
        # Connect to an existing database
        conn = psycopg2.connect(host="localhost", database="jmsbook", user=os.getenv("postgres_user"),
                                password=os.getenv("postgres_pass"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break

    except Exception as error:
        print("Connection to database failed!")
        print(f"Error: {error}")
        time.sleep(2)


my_posts = [{"title": "I get my drinks in California",
             "content": "ooo that's it",
             "id": 1},
            {"title": "I hurt myself at night",
             "content": "I think I am not okay",
             "id": 2}
            ]


def find_post(id):
    output = [x if x["id"] == id else None for x in my_posts]
    return output[0]


def find_post_index(id):
    output = [i if x["id"] == id else None for i, x in enumerate(my_posts)]
    return output[0]


@app.get("/")
def read_root():
    return {"message": "welcome to my API"}






