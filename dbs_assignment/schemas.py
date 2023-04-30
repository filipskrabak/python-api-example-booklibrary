from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    id:str
    personal_identificator:str
    email:str
    name:str
    surname:str
    birth_date:str

class PatchUserRequest(BaseModel):
    personal_identificator:str = None
    email:str = None
    name:str = None
    surname:str = None
    birth_date:str = None

