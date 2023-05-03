import datetime
import uuid
from pydantic import BaseModel, EmailStr, validator

class CreateUserRequest(BaseModel):
    id:uuid.UUID = None
    personal_identificator:str
    email:EmailStr
    name:str
    surname:str
    birth_date: datetime.date # example: 2019-08-24

class PatchUserRequest(BaseModel):
    personal_identificator:str = None
    email:EmailStr = None
    name:str = None
    surname:str = None
    birth_date:datetime.date = None

class CreateCardRequest(BaseModel):
    id:uuid.UUID = None
    user_id:uuid.UUID
    magstripe:str
    status:str

    @validator('status')
    def status_must_be_enum(cls, v):
        if v not in ['active', 'inactive', 'expired']:
            raise ValueError('Status enum must be one of the following: active, inactive, expired')
        return v

class PatchCardRequest(BaseModel):
    user_id:uuid.UUID = None
    status:str = None

    @validator('status')
    def status_must_be_enum(cls, v):
        if v not in ['active', 'inactive', 'expired']:
            raise ValueError('Status enum must be one of the following: active, inactive, expired')
        return v

class CreatePublicationRequest(BaseModel):
    id:uuid.UUID = None
    title:str
