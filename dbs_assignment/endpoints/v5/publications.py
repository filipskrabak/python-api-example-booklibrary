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

@router.get("/publications/{publicationId}")
async def get_publication(publicationId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Publication).filter(models.Publication.id == publicationId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Publication Not Found")

    return {
        "id": result.id,
        "title": result.title,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.post("/publications", status_code=status.HTTP_201_CREATED)
async def create_publication(input: schemas.CreatePublicationRequest, db: Session = Depends(database.get_conn)):
    # Check for duplicates
    if input.id and db.query(models.Publication).filter(models.Publication.id == input.id).first():
        raise HTTPException(status_code=409, detail="This publication already exists!")
    elif input.id is None:
        input.id = uuid.uuid4() # generate an UUID if not provided

    to_create = models.Publication(
        id=input.id,
        title=input.title,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "title": to_create.title,
        "created_at": to_create.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": to_create.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }
