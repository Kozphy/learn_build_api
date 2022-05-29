from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):

    title: str
    content: str
    published: bool = True

my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
     },
     {
         "title": "favorite foods",
         "content": "pizza, pasta, burger",
         "id": 2,
     }
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    print(post)
    return {"data": f"{post}"}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the aarray that has required ID 
    # my_posts.pop(i)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data': post_dict}