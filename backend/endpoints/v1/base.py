from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/status")
async def status():
    return {"status": "OK"}
