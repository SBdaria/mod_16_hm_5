from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int
    username: str
    age: int

@app.get('/')
async def get_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})


@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        for i in users:
            if i.id == user_id:
                return templates.TemplateResponse('users.html', {'request': request, 'user': i})
        raise Exception
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")


@app.post('/user/{username}/{age}')
async def add_in_dict(
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='DariDari')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='27')]) -> User:
    if users:
        edit_user = User(id = users[-1].id + 1, username = username, age = age)
    else:
        edit_user = User(id = 1, username = username, age = age)
    users.append(edit_user)
    return edit_user


@app.put('/user/{user_id}/{username}/{age}')
async def update_dict(user_id: Annotated[int, Path(description='Enter ID', example='1')],
                      username: Annotated[
                          str, Path(min_length=5, max_length=20, description='Enter username', example='DariDari')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='27')]) -> User:
    try:
        for i in users:
            if i.id == user_id:
                i.username = username
                i.age = age
                return i
        raise Exception
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(description='Enter ID', example='1')]) -> User:
    try:
        for i in users:
            if i.id == user_id:
                users.remove(i)
                return i
        raise Exception
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
