from fastapi import APIRouter

from src import namespaces

router = APIRouter()


@router.get("/all")
async def get_all_dns_zones() -> dict:
    return await namespaces.get_all_zones()
