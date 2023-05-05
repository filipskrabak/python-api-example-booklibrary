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

@router.get("/cards/{cardId}")
async def get_card(cardId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Card).filter(models.Card.id == cardId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Not Found")

    return {
        "id": result.id,
        "user_id": result.user_id,
        "magstripe": result.magstripe,
        "status": result.status,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.post("/cards", status_code=status.HTTP_201_CREATED)
async def create_card(input: schemas.CreateCardRequest, db: Session = Depends(database.get_conn)):
    # Check for duplicates
    if input.id and db.query(models.Card).filter(models.Card.id == input.id).first():
        raise HTTPException(status_code=409, detail="This Card ID already exists")
    elif input.id is None:
        input.id = uuid.uuid4()

    # Check if this user already has a card
    if db.query(models.Card).filter(models.Card.user_id == input.user_id).first():
        raise HTTPException(status_code=409, detail="Card for this user already exists")

    # Check if user ID exists
    if db.query(models.User).filter(models.User.id == input.user_id).first() is None:
        raise HTTPException(status_code=404, detail="User ID not found")

    to_create = models.Card(
        id=input.id,
        user_id=input.user_id,
        magstripe=input.magstripe,
        status=input.status,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "user_id": to_create.user_id,
        "magstripe": to_create.magstripe,
        "status": to_create.status,
        "created_at": to_create.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": to_create.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.patch("/cards/{cardId}")
async def update_card(cardId: str, input: schemas.PatchCardRequest, db: Session = Depends(database.get_conn)):
    result = db.query(models.Card).filter(models.Card.id == cardId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Not Found")

    if input.status:
        result.status = input.status

    result.updated_at = datetime.datetime.now()
    db.commit()

    return {
        "id": result.id,
        "user_id": result.user_id,
        "magstripe": result.magstripe,
        "status": result.status,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.delete("/cards/{cardId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(cardId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Card).filter(models.Card.id == cardId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Not Found")

    db.delete(result)
    db.commit()

    return
