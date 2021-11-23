from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, find_dotenv
import os
import time
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


load_dotenv(find_dotenv())


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(f"""INSERT INTO posts (title, content, published)
    # VALUES ({post.title}, {post.content}, {post.published}); """)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * ; """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    models.Post(title=post.title, content=post.content, published=post.published)

    return {"data": new_post} # 5:10:40
# title: str, content: str


@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    test_post = cursor.fetchone()
    print(test_post)
    post = find_post(id=id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"item_id": id, "post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * ;""", str(id),)
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    return {"data": updated_post}