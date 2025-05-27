from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes.tickets import router as tickets_router


load_dotenv()
app = FastAPI()
app.include_router(tickets_router)

@app.get("/")
async def root():
    return {"message": "Welcome to JN Tickets!"}