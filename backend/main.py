from fastapi import FastAPI

from routes.auth import router as auth_router
from routes.tasks import router as task_router
from routes.schedule import router as schedule_router
from routes.sessions import router as session_router
from routes.analytics import router as analytics_router
from routes.users import router as user_router

from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(schedule_router)
app.include_router(session_router)
app.include_router(analytics_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Server running"}