from fastapi import FastAPI, Path
from typing import Annotated
from fastapi import HTTPException

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")         # возвращает словарь users
async def get_users() ->dict:
    return users

@app.post('/user/{username}/{age}')     # Добавление пользователя
async def user_post(
    username: Annotated
    [str,Path(
        min_length=5,
        max_length=15,
        description='Имя пользователя (от 5 до 20 символов)',
        example = "Petrovich"
      )
    ],
    age: Annotated[
    int,Path(
        gt=18,
        le=120,
        description="Введите свой возраст (от 18 до 120)"
      )
    ]
) -> str:
    if users:                           # Добавляем пользователя
        user_id = str(int(max(users, key=int))+1)
    else:
        user_id = '1'     # Начинаем с 1, если словарь пустой
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} is registered'

@app.put('/user/{user_id}/{username}/{age}') # Замена пользователя по [user_id]
async def update_users(
    user_id:Annotated[
        str,Path(
        ge=1,
        le=100,
        description='Введите ID пользователя (строка от 1 до 100)'
        )
      ],
    username:Annotated[
        str,Path(
        min_length=5,
        max_length=20,
        description='Имя пользователя (от 5 до 20 символов)'
      )
    ],
    age:Annotated[
        int,Path(
        gt = 18,
        le=120,
        description="Введите свой возраст (от 18 до 120)"
      )
    ]
) ->str:
                # Обновляем данные пользователя
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is registered'

@app.delete('/user/{user_id}')
async def delete_user(
    user_id:Annotated[
    str,Path(
        ge=1,
        le=100,
        description='Введите ID пользователя (строка от 1 до 100)'
      )
    ]
)-> str:
    users.pop(user_id)   # Удаляем пользователя
    return f'User {user_id} has been deleted'

#  блок кода ниже (по запросу delete) не отрабатывает на FastAPI ???

# @app.delete('/user/{user_id}')
# async def delete_user(user_id: int) -> str:
#     for i, user in enumerate(users):
#         if user['id'] == user_id:
#             del users[i]           # Удаляем пользователя по users[i]
#     return f'User {user_id} has been deleted'



#   uvicorn module_16_3:app --reload
#   http://127.0.0.1:8000/users
#   http://127.0.0.1:8000/docs
