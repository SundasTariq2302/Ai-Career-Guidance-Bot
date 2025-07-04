from fastapi import APIRouter

router = APIRouter()

# Test route
@router.get("/status")
async def get_status():
    return {"status": "OK", "message": "Career Bot API running smoothly"}
