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

@router.get("/categories/{categoryId}")
async def get_category(categoryId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Category).filter(models.Category.id == categoryId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Category Not Found")

    return {
        "id": result.id,
        "name": result.name,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.post("/categories", status_code=status.HTTP_201_CREATED)
async def create_category(input: schemas.CreateCategoryRequest, db: Session = Depends(database.get_conn)):
    # Check for duplicates
    if input.id and db.query(models.Category).filter(models.Category.id == input.id).first():
        raise HTTPException(status_code=409, detail="This category already exists!")
    elif input.id is None:
        input.id = uuid.uuid4() # generate an UUID if not provided

    # Check for duplicates
    if db.query(models.Category).filter(models.Category.name == input.name).first():
        raise HTTPException(status_code=409, detail="Conflict! This category name already exists.")

    to_create = models.Category(
        id=input.id,
        name=input.name,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "name": to_create.name,
        "created_at": to_create.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": to_create.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.patch("/categories/{categoryId}")
async def update_category(categoryId: str, input: schemas.PatchCategoryRequest, db: Session = Depends(database.get_conn)):
    result = db.query(models.Category).filter(models.Category.id == categoryId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Category Not Found")

    # Check for duplicates
    if db.query(models.Category).filter(models.Category.name == input.name).first():
        raise HTTPException(status_code=409, detail="Conflict! This category name already exists.")

    if(input.name):
        result.name = input.name

    result.updated_at = datetime.datetime.now()
    db.commit()

    return {
        "id": result.id,
        "name": result.name,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.delete("/categories/{categoryId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(categoryId:str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Category).filter(models.Category.id == categoryId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Category Not Found")

    db.delete(result)
    db.commit()

    return
