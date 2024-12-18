from fastapi import APIRouter

from src.utils import get_all_zones

router = APIRouter()


@router.get("/all")
async def get_all_dns_zones() -> dict:
    return await get_all_zones()
