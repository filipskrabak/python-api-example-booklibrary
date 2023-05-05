from fastapi import APIRouter

from dbs_assignment.endpoints.v5 import users
from dbs_assignment.endpoints.v5 import cards
from dbs_assignment.endpoints.v5 import publications
from dbs_assignment.endpoints.v5 import authors
from dbs_assignment.endpoints.v5 import categories
from dbs_assignment.endpoints.v5 import instances

router = APIRouter()

router.include_router(users.router, tags=["users"])
router.include_router(cards.router, tags=["cards"])
router.include_router(authors.router, tags=["authors"])
router.include_router(publications.router, tags=["publications"])
router.include_router(categories.router, tags=["categories"])
router.include_router(instances.router, tags=["instances"])
