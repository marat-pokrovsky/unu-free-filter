from fastapi import APIRouter

from .sorting import router as sorting_router
from .data_structures import router as ds_router

router = APIRouter()

router.include_router(sorting_router, prefix="/sorting")
router.include_router(ds_router, prefix="/data-structures")
