""" Copyright (C) 2020, 2021 Alex Visca

WebAPI Program
"""
import uvicorn as server
from fastapi import FastAPI


from routers import homepage, api
from src import database as db


def init_app():
    app = FastAPI()
    # include routers
    app.include_router(router=homepage.router)
    app.include_router(router=api.router)
    # TODO: include middleware
    # --
    return app


def main():
    db.session()
    server.run(
        "main:init_app", 
        factory=True,
        reload=False, 
        access_log=True)


if __name__ == '__main__':
    main()
