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
        raise HTTPException(status_code=400, detail="User Not Found (ID invalid)")

    # Check if publication ID is valid
    if not db.query(models.Publication).filter(models.Publication.id == input.publication_id).first():
        raise HTTPException(status_code=400, detail="Publication Not Found (ID invalid)")

    # Get publication model
    publication = db.query(models.Publication).filter(models.Publication.id == input.publication_id).first()

    # Check if publication has available instances
    instance = db.query(models.Instance).filter(models.Instance.publication_id == publication.id, models.Instance.status == 'available').first()

    if not instance:
        raise HTTPException(status_code=400, detail="No available instances for this publication")

    #  If there are some reservations for the publication, only first user in the queue is able to create a rental
    if db.query(models.Reservation).filter(models.Reservation.publication_id == publication.id).first():
        # queue ordered by reservation created_at
        queue = db.query(models.Reservation).filter(models.Reservation.publication_id == publication.id).order_by(models.Reservation.created_at.asc()).all()
        if queue[0].user_id != input.user_id:
            raise HTTPException(status_code=400, detail="The user is not first in the queue")

    # Set instance status to reserved
    instance.status = "reserved"

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

@router.patch("/rentals/{rentalId}")
async def update_rental(rentalId: str, input: schemas.PatchRentalRequest, db: Session = Depends(database.get_conn)):
    result = db.query(models.Rental).filter(models.Rental.id == rentalId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Rental Not Found")

    # check if rental is active
    if result.status != 'active':
        raise HTTPException(status_code=400, detail="Rental is not active")

    result.duration = input.duration
    result.end_date = datetime.datetime.now() + datetime.timedelta(days=input.duration)

    db.commit()

    return {
        "id": result.id,
        "user_id": result.user_id,
        "publication_instance_id": result.instance_id,
        "duration": result.duration,
        "start_date": result.start_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "end_date": result.end_date.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "status": result.status
    }
