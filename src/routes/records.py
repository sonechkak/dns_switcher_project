from fastapi import APIRouter

from src.namespaces import get_min_dns_records, update_existing_record, get_records, delete_record_by_id

router = APIRouter()


@router.get("/all")
async def get_full_dns_records() -> dict:
    return await get_records()


@router.get("/minify")
async def get_minify_dns_records():
    return await get_min_dns_records()

@router.put("/update/")
async def update_dns_record_by_id() -> dict:
    return await update_existing_record()


@router.delete("/delete/")
async def delete_dns_record_by_id() -> dict:
    return await delete_record_by_id()
