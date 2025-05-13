from fastapi import FastAPI
from tasks.routers import router as task_routes
from auth.routers import router as auth_routes
from database.database import create_db_and_tables

app = FastAPI()


app.include_router(task_routes)
app.include_router(auth_routes)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
