from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from route.routes import router

app = FastAPI()

app.include_router(router)
Instrumentator().instrument(app).expose(app)