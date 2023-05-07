import datetime
import uuid
from pydantic import BaseModel, EmailStr, StrictStr, validator, Field

def enum_validator(v, values):
    if v not in values:
        raise ValueError('Status enum must be one of the following: ' + ', '.join(values))
    return v

class AuthorsList(BaseModel):
    name:StrictStr
    surname:StrictStr

class CreateUserRequest(BaseModel):
    id:uuid.UUID = None
    personal_identificator:str
    email:EmailStr
    name:StrictStr
    surname:StrictStr
    birth_date: datetime.date # example: 2019-08-24

class PatchUserRequest(BaseModel):
    personal_identificator:str = None
    email:EmailStr = None
    name:StrictStr = None
    surname:StrictStr = None
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
    title:StrictStr
    authors:list[AuthorsList]
    categories:list[StrictStr]

class PatchPublicationRequest(BaseModel):
    title:StrictStr = None
    authors:list[AuthorsList] = None
    categories:list[StrictStr] = None

class CreateAuthorRequest(BaseModel):
    id:uuid.UUID = None
    name:StrictStr
    surname:StrictStr

class PatchAuthorRequest(BaseModel):
    name:StrictStr = None
    surname:StrictStr = None

class CreateCategoryRequest(BaseModel):
    id:uuid.UUID = None
    name:StrictStr

class PatchCategoryRequest(BaseModel):
    name:StrictStr

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

class CreateRentalRequest(BaseModel):
    id:uuid.UUID = None
    user_id:uuid.UUID
    publication_id:uuid.UUID
    duration:int = Field(..., gt=0, lt=15)

class PatchRentalRequest(BaseModel):
    duration:int = Field(..., gt=0, lt=15)

class CreateReservationRequest(BaseModel):
    id:uuid.UUID = None
    user_id:uuid.UUID
    publication_id:uuid.UUID
