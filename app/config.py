from fastapi import FastAPI
from routers import route_explore, router_search_by_tag, route_search_by_username


app = FastAPI()
app.include_router(route_explore.router, tags=["explore"])
app.include_router(router_search_by_tag.router, tags=["search_by_tag"])
app.include_router(route_search_by_username.router, tags=["search_by_username"])
# app.include_router(route_task_handler.router,tags=['task_handler'])
