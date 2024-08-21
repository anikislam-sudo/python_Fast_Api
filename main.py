from fastapi import FastAPI
from app.controllers import router

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    from app.models import Base
    from app.databases import engine
    Base.metadata.create_all(bind=engine)