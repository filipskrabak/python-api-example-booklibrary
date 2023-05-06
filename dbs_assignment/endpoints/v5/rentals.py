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

@router.get("/rentals/{rentalId}")
async def get_rental(rentalId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Rental).filter(models.Rental.id == rentalId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Rental Not Found")

    return {
        "id": result.id,
        "user_id": result.user_id,
        "publication_instance_id": result.instance_id,
        "duration": result.duration,
        "start_date": result.start_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "end_date": result.end_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "status": result.status
    }

@router.post("/rentals", status_code=status.HTTP_201_CREATED)
async def create_rental(input: schemas.CreateRentalRequest, db: Session = Depends(database.get_conn)):
    # Check for duplicates
    if input.id and db.query(models.Rental).filter(models.Rental.id == input.id).first():
        raise HTTPException(status_code=409, detail="This rental already exists!")
    elif input.id is None:
        input.id = uuid.uuid4() # generate an UUID if not provided

    # Check if user ID is valid
    if not db.query(models.User).filter(models.User.id == input.user_id).first():
        raise HTTPException(status_code=404, detail="User Not Found (ID invalid)")

    # Check if publication ID is valid
    if not db.query(models.Publication).filter(models.Publication.id == input.publication_id).first():
        raise HTTPException(status_code=404, detail="Publication Not Found (ID invalid)")

    # Get publication model
    publication = db.query(models.Publication).filter(models.Publication.id == input.publication_id).first()

    # Check if publication has available instances by ORM relationship
    instance = db.query(models.Instance).filter(models.Instance.publication_id == publication.id, models.Instance.status == 'available').first()

    if not instance:
        raise HTTPException(status_code=400, detail="No available instances for this publication")



    to_create = models.Rental(
        id=input.id,
        user_id=input.user_id,
        instance_id=instance.id,
        duration=input.duration,
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now() + datetime.timedelta(days=input.duration),
        status='active'
    )

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "user_id": to_create.user_id,
        "publication_instance_id": to_create.instance_id,
        "duration": to_create.duration,
        "start_date": to_create.start_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "end_date": to_create.end_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "status": to_create.status
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
