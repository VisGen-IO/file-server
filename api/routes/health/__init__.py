from fastapi import APIRouter
from api.routes.health.health_check import router as health_router
router = APIRouter(prefix="/health")
router.include_router(health_router)