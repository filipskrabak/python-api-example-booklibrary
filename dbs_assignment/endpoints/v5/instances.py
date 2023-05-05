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

@router.get("/instances/{instanceId}")
async def get_instance(instanceId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Instance).filter(models.Instance.id == instanceId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Instance Not Found")

    return {
        "id": result.id,
        "type": result.type,
        "publisher": result.publisher,
        "year": result.year,
        "status": result.status,
        "publication_id": result.publication_id,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.post("/instances", status_code=status.HTTP_201_CREATED)
async def create_instance(input: schemas.CreateInstanceRequest, db: Session = Depends(database.get_conn)):
    # Check for duplicates
    if input.id and db.query(models.Instance).filter(models.Instance.id == input.id).first():
        raise HTTPException(status_code=409, detail="This instance already exists!")
    elif input.id is None:
        input.id = uuid.uuid4() # generate an UUID if not provided

    # Check if publication ID exists
    if not db.query(models.Publication).filter(models.Publication.id == input.publication_id).first():
        raise HTTPException(status_code=400, detail="Publication ID does not exist!")

    to_create = models.Instance(
        id=input.id,
        type=input.type,
        publisher=input.publisher,
        year=input.year,
        status=input.status,
        publication_id=input.publication_id,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "type": to_create.type,
        "publisher": to_create.publisher,
        "year": to_create.year,
        "status": to_create.status,
        "publication_id": to_create.publication_id,
        "created_at": to_create.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": to_create.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.patch("/instances/{instanceId}")
async def update_instance(instanceId: str, input: schemas.PatchInstanceRequest, db: Session = Depends(database.get_conn)):
    result = db.query(models.Instance).filter(models.Instance.id == instanceId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Instance Not Found")

    if input.type:
        result.type = input.type

    if input.publisher:
        result.publisher = input.publisher

    if input.year:
        result.year = input.year

    if input.status:
        result.status = input.status

    if input.publication_id:
        if not db.query(models.Publication).filter(models.Publication.id == input.publication_id).first():
            raise HTTPException(status_code=400, detail="Publication ID does not exist!")
        else:
            result.publication_id = input.publication_id

    result.updated_at = datetime.datetime.now()
    db.commit()

    return {
        "id": result.id,
        "type": result.type,
        "publisher": result.publisher,
        "year": result.year,
        "status": result.status,
        "publication_id": result.publication_id,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.delete("/instances/{instanceId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instance(instanceId:str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Instance).filter(models.Instance.id == instanceId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Instance Not Found")

    db.delete(result)
    db.commit()

    return
