from fastapi import APIRouter

from database import SQL, Connect, Country, City

router = APIRouter()


@router.get("/version")
def version():
    with Connect() as cursor:
        version = SQL.version(cursor)
    return version

@router.get("/index")
def lookup(item_id: int):
    with Connect() as cursor:
        raw_data = SQL.lookup(cursor, item_id)
    result = City.construct(raw_data)
    return result.__dict__

@router.get("/search")
def search(query: str):
    with Connect() as cursor:
        raw_data = SQL.search(cursor, query)
    result = Country.construct(raw_data)
    return result.__dict__

