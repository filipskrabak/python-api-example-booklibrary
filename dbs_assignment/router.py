from fastapi import APIRouter

# v5
from dbs_assignment.endpoints.v5 import users
from dbs_assignment.endpoints.v5 import cards

router = APIRouter()

# v5
router.include_router(users.router, tags=["users"])
router.include_router(cards.router, tags=["cards"])
