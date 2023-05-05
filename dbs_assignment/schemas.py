import datetime
import uuid
from pydantic import BaseModel, EmailStr, validator

def enum_validator(v, values):
    if v not in values:
        raise ValueError('Status enum must be one of the following: ' + ', '.join(values))
    return v

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

    _validate_status = validator('status', allow_reuse=True)(lambda v: enum_validator(v, ['active', 'inactive', 'expired']))

class PatchCardRequest(BaseModel):
    user_id:uuid.UUID = None
    status:str = None

    _validate_status = validator('status', allow_reuse=True)(lambda v: enum_validator(v, ['active', 'inactive', 'expired']))

class CreatePublicationRequest(BaseModel):
    id:uuid.UUID = None
    title:str

class CreateAuthorRequest(BaseModel):
    id:uuid.UUID = None
    name:str
    surname:str

class PatchAuthorRequest(BaseModel):
    name:str = None
    surname:str = None

class CreateCategoryRequest(BaseModel):
    id:uuid.UUID = None
    name:str

class PatchCategoryRequest(BaseModel):
    name:str = None

class CreateInstanceRequest(BaseModel):
    id:uuid.UUID = None
    type:str
    publisher:str
    year:int
    status:str
    publication_id:uuid.UUID

    _validate_type = validator('type', allow_reuse=True)(lambda v: enum_validator(v, ['physical', 'ebook', 'audiobook']))

    _validate_status = validator('status', allow_reuse=True)(lambda v: enum_validator(v, ['available', 'reserved']))

class PatchInstanceRequest(BaseModel):
    type:str = None
    publisher:str = None
    year:int = None
    status:str = None
    publication_id:uuid.UUID = None

    _validate_type = validator('type', allow_reuse=True)(lambda v: enum_validator(v, ['physical', 'ebook', 'audiobook']))

    _validate_status = validator('status', allow_reuse=True)(lambda v: enum_validator(v, ['available', 'reserved']))
