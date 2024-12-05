from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    description: str
    isApproved: bool = False
    review: Optional[int] = None

my_post = [
    {
        'id': 1,
        'title': 'Post 1 title',
        'description': 'Post 1 description'
    },
    {
        'id': 2,
        'title': 'Post 2 title',
        'description': 'Post 2 description'
    }
]

def find_post_id(id):
    for p in my_post:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get('/posts')
def get_all_posts():
    return {'data': my_post}

@app.post('/post')
def create_post(post: Post, status_code = status.HTTP_201_CREATED):
    post_to_dict = post.dict()
    post_to_dict['id'] = randrange(0, 100)
    my_post.append(post_to_dict)
    return {'data': my_post}

@app.get('/post/{id}')
def get_single_post(id: int):
    post = find_post_id(id)
    if not post:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Post id: {id} is not found.'
        )
    return {'data': post}

@app.delete('/post/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post id: {id} was not found'
            )
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/post/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Post id {id} was not found'
        )
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[index] = post_dict
    return {'data': post_dict}