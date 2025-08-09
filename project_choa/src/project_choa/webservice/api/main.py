# import library
from fastapi import FastAPI
from pydantic import BaseModel

# create object app FastApi
app = FastAPI()


# function '/'
@app.get('/')
def root():
    return {'message': 'Hello FastAPI'}


# function 'about'
@app.get('/about')
def about():
    return {'message': '초아, AI for finance'}


