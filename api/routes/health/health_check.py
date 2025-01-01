from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/")
async def health():
    return {"status": "Service is so beautiful, so elegant just running like a wow"}

@router.head("/")
async def health():
    return JSONResponse(content={"status": "File server is up"}, status_code=200)