from fastapi import APIRouter

# v5
from dbs_assignment.endpoints.v5 import users

router = APIRouter()

# v5
router.include_router(users.router, tags=["users"])
