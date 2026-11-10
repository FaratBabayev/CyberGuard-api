from fastapi import FastAPI

from app.errors import register_error_handlers
from app.routes import greeting, incidents

app = FastAPI(
    title="CyberGuard API",
    description="Mocked-backend prototype (Assignment 2). Data resets on restart.",
    version="1.0.0",
)

register_error_handlers(app)
app.include_router(greeting.router)
app.include_router(incidents.router)
