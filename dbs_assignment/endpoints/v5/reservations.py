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

@router.get("/reservations/{reservationId}")
async def get_reservation(reservationId: str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Reservation).filter(models.Reservation.id == reservationId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Reservation Not Found")

    return {
        "id": result.id,
        "user_id": result.user_id,
        "publication_id": result.publication_id,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
    }

@router.post("/reservations", status_code=status.HTTP_201_CREATED)
async def create_reservation(input: schemas.CreateReservationRequest, db: Session = Depends(database.get_conn)):
    # Check for duplicates
    if input.id and db.query(models.Reservation).filter(models.Reservation.id == input.id).first():
        raise HTTPException(status_code=409, detail="This reservation ID already exists!")
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

    # Check if publication has available instances
    instance = db.query(models.Instance).filter(models.Instance.publication_id == publication.id, models.Instance.status == 'available').first()

    if instance:
        raise HTTPException(status_code=400, detail="Publication has some instances available to rent!")

    to_create = models.Reservation(
        id=input.id,
        user_id=input.user_id,
        publication_id=publication.id,
        created_at=datetime.datetime.now()
    )

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "user_id": to_create.user_id,
        "publication_id": to_create.publication_id,
        "created_at": to_create.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.delete("/reservations/{reservationId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(reservationId:str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Reservation).filter(models.Reservation.id == reservationId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Reservation Not Found")

    db.delete(result)
    db.commit()

    return
