""" Copyright (C) 2020, 2021 Alex Visca

WebAPI Program
"""
import uvicorn as server
from fastapi import FastAPI


from routers import homepage, api
from src import database as db


app = FastAPI()

def configure_routers():
    app.include_router(router=homepage.router)
    app.include_router(router=api.router)

configure_routers()


def main():
    db.session()


if __name__ == '__main__':
    main()
    server.run(
        "main:app", reload=True, access_log=True)
