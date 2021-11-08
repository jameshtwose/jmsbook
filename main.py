from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

my_posts = [{"title": "I get my drinks in California",
             "content": "ooo that's it",
             "id": 1},
            {"title": "I hurt myself at night",
             "content": "I think I am not okay",
             "id": 2}
            ]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


def find_post(id):
    output = [x if x["id"] == id else None for x in my_posts]
    return output[0]


def find_post_index(id):
    output = [i if x["id"] == id else None for i, x in enumerate(my_posts)]
    return output[0]


@app.get("/")
def read_root():
    return {"message": "welcome to my API"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}
# title: str, content: str


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id=id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"item_id": id, "post": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_post_index(id)
    my_posts.pop(index)
    return {"message": "post was successfully deleted"}