from fastapi import FastAPI
import time
import uvicorn as server


from database import SQL, Connect, Country
from views import routes

app = FastAPI()

def configure_routers():
    # app.include_router(router=routes.router)
    pass

configure_routers()

@app.get("/")
def root():
    with Connect() as db:
        cursor = db.cursor()
        version = SQL.version(cursor)
    return version

@app.get("/<item_id>")
def lookup(item_id: int):
    with Connect() as db:
        cursor = db.cursor()
        result = SQL.lookup(cursor, item_id)
    return result

@app.get("/search")
def search(query: str):
    with Connect() as db:
        cursor = db.cursor()
        raw_data = SQL.search(cursor, query)
    result = Country.construct(raw_data)
    return result.__dict__

def session():
    while True:
        try:
            with Connect() as db:
                cursor = db.cursor()
                version = SQL.version(cursor)
            break
        except Exception as error:
            print("Error: ", error)
            time.sleep(2)
    return version['version']

# Main runtime
def main():
    version = session() # If cannot connect to database, will await connection
    sys_out = F"INFO:\t  Database running on MySQL v{version}"
    print(sys_out)
    # print(search(query='Canada'))


if __name__ == '__main__':
    main()
    server.run(
        "main:app", 
        reload=True, 
        access_log=True)
