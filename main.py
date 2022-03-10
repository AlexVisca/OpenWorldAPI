from fastapi import FastAPI
import uvicorn as server

from views import routes

app = FastAPI()

def configure():
    app.include_router(router=routes.router)

configure()
if __name__ == '__main__':
    server.run(app)
