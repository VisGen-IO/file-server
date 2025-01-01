from fastapi import APIRouter
from .s3_file_ops import router as s3_file_router

router = APIRouter(prefix='/assets')
router.include_router(s3_file_router)