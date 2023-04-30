import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException

from dbs_assignment.config import settings
from dbs_assignment import database
from dbs_assignment import models
from dbs_assignment import schemas

from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users/{userId}")
async def get_user_by_id(userId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.User).filter(models.User.id == userId).first()

    if not result:
        raise HTTPException(status_code=404, detail="User Not Found")

    return {
        "id": result.id,
        "name": result.name,
        "surname": result.surname,
        "email": result.email,
        "birth_date": result.birth_date,
        "personal_identificator": result.identification_num,
        "reservations": [],
        "rentals": [],
        "created_at": result.created_at,
        "updated_at": result.updated_at
    }

@router.post("/users")
async def get_user_by_id(input: schemas.CreateUserRequest, db: Session = Depends(database.get_conn)):
    # Check if user doesn't exist by email
    if db.query(models.User).filter(models.User.email == input.email).first():
        raise HTTPException(status_code=409, detail="Email Already Taken")

    # Check if user doesn't exist by personal_identificator
    if db.query(models.User).filter(models.User.identification_num == input.personal_identificator).first():
        raise HTTPException(status_code=409, detail="Personal Identificator Already Taken")


    to_create = models.User(
        id=input.id,
        identification_num=input.personal_identificator,
        email=input.email,
        name=input.name,
        surname=input.surname,
        birth_date=input.birth_date,
        created_at= datetime.datetime.now(),
        updated_at= datetime.datetime.now()
    )
    db.add(to_create)
    db.commit()
    return {
        "id": to_create.id,
        "personal_identificator": to_create.identification_num,
        "email": to_create.email,
        "name": to_create.name,
        "surname": to_create.surname,
        "birth_date": to_create.birth_date,
        "created_at": to_create.created_at,
        "updated_at": to_create.updated_at
    }

@router.patch("/users/{userId}")
async def get_user_by_id(userId: str, input: schemas.PatchUserRequest, db: Session = Depends(database.get_conn)):
    result = db.query(models.User).filter(models.User.id == userId).first()

    if not result:
        raise HTTPException(status_code=404, detail="User Not Found")

    # Check if user doesn't exist by email
    if db.query(models.User).filter(models.User.email == input.email).first():
        raise HTTPException(status_code=409, detail="Email Already Taken")

    # Check if user doesn't exist by personal_identificator
    if db.query(models.User).filter(models.User.identification_num == input.personal_identificator).first():
        raise HTTPException(status_code=409, detail="Personal Identificator Already Taken")

    if(input.personal_identificator):
        result.identification_num = input.personal_identificator

    if(input.email):
        result.email = input.email

    if(input.name):
        result.name = input.name

    if(input.surname):
        result.surname = input.surname

    if(input.birth_date):
        result.birth_date = input.birth_date

    result.updated_at = datetime.datetime.now()
    db.commit()

    return {
        "id": result.id,
        "personal_identificator": result.identification_num,
        "email": result.email,
        "name": result.name,
        "surname": result.surname,
        "birth_date": result.birth_date,
        "created_at": result.created_at,
        "updated_at": result.updated_at
    }
