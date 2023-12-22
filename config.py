from fastapi import FastAPI
from app.routers import explore, search_by_username
from app.routers import search_by_tag


app = FastAPI()
app.include_router(explore.router, tags=["explore"])
app.include_router(search_by_tag.router, tags=["search_by_tag"])
app.include_router(search_by_username.router, tags=["search_by_username"])
# app.include_router(route_task_handler.router,tags=['task_handler'])
