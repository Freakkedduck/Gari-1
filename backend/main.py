from fastapi import FastAPI
from routes.upload import router as upload_router

app = FastAPI(title="DocBot API")

app.include_router(upload_router, prefix="/api")

