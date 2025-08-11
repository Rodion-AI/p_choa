# import library
from fastapi import FastAPI
from pydantic import BaseModel
from project_choa.webservice.api.choaAI import ChoaAI

# create object app FastApi
app = FastAPI()
# create object AI LLM
choa = ChoaAI()


# class for data
class NeuroRequest(BaseModel):
    """Модель запроса для нейро-финансиста."""
    note: str

# function '/'
@app.get('/')
def root():
    return {'message': 'Hello FastAPI'}

# function 'about'
@app.get('/about')
def about():
    return {'message': '초아, AI for finance'}

# function 'neuro'
@app.post('/api/neuro/')
def neuro(request: NeuroRequest):
    return choa.neuro_finansist(request.note)

