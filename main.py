from fastapi import FastAPI
import time
import uvicorn as server


# Application imports
import database as db
from views import homepage, api

app = FastAPI()

def configure_routers():
    app.include_router(router=homepage.router)
    app.include_router(router=api.router)

configure_routers()


# Main runtime
def main():
    version = db.session() # If cannot connect to database, will await connection
    sys_out = F"INFO:\t  Database running on MySQL v{version['version']}"
    print(sys_out)


if __name__ == '__main__':
    main()
    server.run(
        "main:app", 
        reload=True, 
        access_log=True)
