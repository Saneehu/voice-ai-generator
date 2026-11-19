from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import config
from routes import router

app = FastAPI(title="Voice Translator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.mount("/output", StaticFiles(directory=config.OUTPUT_DIR), name="output")
# Must be last: serves the frontend at http://localhost:8000/
app.mount("/", StaticFiles(directory=config.FRONTEND_DIR, html=True), name="frontend")