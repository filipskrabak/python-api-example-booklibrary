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

@router.get("/authors/{authorId}")
async def get_author(authorId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Author).filter(models.Author.id == authorId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Author Not Found")

    return {
        "id": result.id,
        "name": result.name,
        "surname": result.surname,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.post("/authors", status_code=status.HTTP_201_CREATED)
async def create_author(input: schemas.CreateAuthorRequest, db: Session = Depends(database.get_conn)):
    # Check for duplicates
    if input.id and db.query(models.Author).filter(models.Author.id == input.id).first():
        raise HTTPException(status_code=409, detail="This author already exists!")
    elif input.id is None:
        input.id = uuid.uuid4() # generate an UUID if not provided

    to_create = models.Author(
        id=input.id,
        name=input.name,
        surname=input.surname,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "name": to_create.name,
        "surname": to_create.surname,
        "created_at": to_create.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": to_create.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.patch("/authors/{authorId}")
async def update_author(authorId: str, input: schemas.PatchAuthorRequest, db: Session = Depends(database.get_conn)):
    result = db.query(models.Author).filter(models.Author.id == authorId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Author Not Found")

    if(input.name):
        result.name = input.name

    if(input.surname):
        result.surname = input.surname

    result.updated_at = datetime.datetime.now()
    db.commit()

    return {
        "id": result.id,
        "name": result.name,
        "surname": result.surname,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.delete("/authors/{authorId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(authorId:str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Author).filter(models.Author.id == authorId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Author Not Found")

    db.delete(result)
    db.commit()

    return
