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

    authors_json = []
    categories_json = []

    for author in result.authors:
        authors_json.append({"name": author.name, "surname": author.surname})

    for category in result.categories:
        categories_json.append(category.name)

    return {
        "id": result.id,
        "title": result.title,
        "authors": authors_json,
        "categories": categories_json,
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

    authors_json = []
    categories_json = []

    to_create = models.Publication(
        id=input.id,
        title=input.title,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )

    for author in input.authors:
        author_db = db.query(models.Author).filter(models.Author.name == author['name'], models.Author.surname == author['surname']).first()

        if not author_db:
            raise HTTPException(status_code=400, detail=f"Author {author['name']} {author['surname']} not found in the database")

        # assign the author id to the publication
        to_create.authors.append(author_db)
        authors_json.append({"name": author_db.name, "surname": author_db.surname})

    for category in input.categories:
        category_db = db.query(models.Category).filter(models.Category.name == category).first()

        if not category_db:
            raise HTTPException(status_code=400, detail=f"Category {category} not found in the database")

        # assign the category id to the publication
        to_create.categories.append(category_db)
        categories_json.append(category_db.name)

    db.add(to_create)
    db.commit()

    return {
        "id": to_create.id,
        "title": to_create.title,
        "authors": authors_json,
        "categories": categories_json,
        "created_at": to_create.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": to_create.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.patch("/publications/{publicationId}")
async def update_publication(publicationId: str, input: schemas.PatchPublicationRequest, db: Session = Depends(database.get_conn)):
    result = db.query(models.Publication).filter(models.Publication.id == publicationId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Publication Not Found")

    if(input.title):
        result.title = input.title

    if(input.authors):
        # Remove previous authors
        result.authors = []

        for author in input.authors:
            author_db = db.query(models.Author).filter(models.Author.name == author['name'], models.Author.surname == author['surname']).first()

            if not author_db:
                raise HTTPException(status_code=404, detail=f"Author {author['name']} {author['surname']} not found in the database")

            # assign the author id to the publication
            result.authors.append(author_db)

    if(input.categories):
        # Remove previous categories
        result.categories = []

        for category in input.categories:
            category_db = db.query(models.Category).filter(models.Category.name == category).first()

            if not category_db:
                raise HTTPException(status_code=404, detail=f"Category {category} not found in the database")

            # assign the category id to the publication
            result.categories.append(category_db)

    authors_json = []
    categories_json = []

    for author in result.authors:
        authors_json.append({"name": author.name, "surname": author.surname})

    for category in result.categories:
        categories_json.append(category.name)

    result.updated_at = datetime.datetime.now()
    db.commit()

    return {
        "id": result.id,
        "title": result.title,
        "authors": authors_json,
        "categories": categories_json,
        "created_at": result.created_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z',
        "updated_at": result.updated_at.replace(tzinfo=None).isoformat(timespec='milliseconds') + 'Z'
    }

@router.delete("/publications/{publicationId}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_publication(publicationId:str, db: Session = Depends(database.get_conn)):
    result = db.query(models.Publication).filter(models.Publication.id == publicationId).first()

    if not result:
        raise HTTPException(status_code=404, detail="Publication Not Found")

    db.delete(result)
    db.commit()

    return
