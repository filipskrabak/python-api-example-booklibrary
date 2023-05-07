from datetime import date
import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException, status

from dbs_assignment.config import settings
from dbs_assignment import database
from dbs_assignment import models
from dbs_assignment import schemas

from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users/{userId}")
async def get_user(userId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.User).filter(models.User.id == userId).first()

    if not result:
        raise HTTPException(status_code=404, detail="User Not Found")

    if(result.email is None):
        parent = db.query(models.User).filter(models.User.id == result.parent_id).first()
        result.email = parent.email

    reservations = []
    rentals = []

    for reservation in result.reservations:
        reservations.append({
            "id": reservation.id,
            "user_id": reservation.user_id,
            "publication_id": reservation.publication_id,
            "created_at": reservation.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        })

    for rental in result.rentals:
        rentals.append({
            "id": rental.id,
            "user_id": rental.user_id,
            "publication_instance_id": rental.instance_id,
            "duration": rental.duration,
            "start_date": rental.start_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
            "end_date": rental.end_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
            "status": rental.status,
        })

    to_return = {
        "id": result.id,
        "name": result.name,
        "surname": result.surname,
        "email": result.email,
        "birth_date": result.birth_date,
        "personal_identificator": result.identification_num,
        "reservations": reservations,
        "rentals": rentals,
        "created_at": result.created_at,
        "updated_at": result.updated_at
    }

    if(len(reservations) == 0):
        del to_return["reservations"]

    if(len(rentals) == 0):
        del to_return["rentals"]

    return to_return

@router.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(input: schemas.CreateUserRequest, db: Session = Depends(database.get_conn)):
    parent_id = None

    # Check if user doesn't exist by id
    if input.id and db.query(models.User).filter(models.User.id == input.id).first():
        raise HTTPException(status_code=409, detail="User Already Exists")
    elif input.id is None:
        input.id = uuid.uuid4()

    # Check if user doesn't exist by email
    email_query = db.query(models.User).filter(models.User.email == input.email).first()

    if email_query:
        # Check if the new user is a child
        if(get_age(input.birth_date) < 18):
            parent_id = email_query.id
            input.email = None
        else:
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
        parent_id=parent_id,
        birth_date=input.birth_date,
        created_at= datetime.datetime.now(),
        updated_at= datetime.datetime.now()
    )
    db.add(to_create)
    db.commit()

    if(input.email is None):
        to_create.email = email_query.email

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
async def update_user(userId: str, input: schemas.PatchUserRequest, db: Session = Depends(database.get_conn)):
    parent_id = None

    result = db.query(models.User).filter(models.User.id == userId).first()

    if not result:
        raise HTTPException(status_code=404, detail="User Not Found")

    # Check if user doesn't exist by email
    email_query = db.query(models.User).filter(models.User.email == input.email).first()

    if email_query:
        # Check if the new user is a child
        person_age = None

        # Check whether the user entered a birth date
        if(input.birth_date):
            person_age = get_age(input.birth_date)
        else:
            person_age = get_age(result.birth_date)

        if(person_age < 18):
            parent_id = email_query.id
            input.email = None
        else:
            raise HTTPException(status_code=409, detail="Email Already Taken")

    # Check if user doesn't exist by personal_identificator
    if db.query(models.User).filter(models.User.identification_num == input.personal_identificator).first():
        raise HTTPException(status_code=409, detail="Personal Identificator Already Taken")

    if(input.personal_identificator):
        result.identification_num = input.personal_identificator

    if(input.email):
        result.email = input.email
        result.parent_id = None

    if(input.name):
        result.name = input.name

    if(input.surname):
        result.surname = input.surname

    if(input.birth_date):
        result.birth_date = input.birth_date

    if(parent_id is not None):
        result.parent_id = parent_id
        result.email = None

    result.updated_at = datetime.datetime.now()
    db.commit()

    if(result.email is None):
        result.email = email_query.email

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

def get_age(date_of_birth):
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
