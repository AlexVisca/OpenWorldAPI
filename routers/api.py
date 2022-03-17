from fastapi import APIRouter, HTTPException, status

from src.database import Connect
from src.models import SQL, CountryProfile

router = APIRouter()


@router.get("/index")
def lookup():
    with Connect() as cursor:
        index = SQL.select_index(cursor)
    return index

@router.get("/search")
def search(query: str):
    try:
        profile = CountryProfile.creator(query)
        return profile

    except Exception as exc:
        message = {"status_code": 404, "message": str(exc)}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=message)
    
