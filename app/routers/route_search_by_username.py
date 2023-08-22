from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import session
from schemes import (
    scheme_search_username as schemes,
    scheme_task_handler,
    scheme_response_username,
)
from models import model_search_username as models, model_get_content, model_mongo_db
from dependencies import get_db


router = APIRouter()


# a POST endpoint for creating a topic
@router.post("/search/username/")
def create_topic(username: schemes.search_username, db: session = Depends(get_db)):
    new_content_request = model_get_content.get_content(
        statistic=username.statistic,
        description=username.description,
        comments=username.comments,
        tags=username.tags,
    )
    task_handler = models.task_handler_username(
        is_active=True, last_status="create task ", is_done=False, crawler_id=0
    )

    new_request = models.requests_model_search_username(
        username=username.username,
        quantity=username.quantity,
        content=new_content_request,
        task_handler=task_handler,
    )
    db.add(new_request)
    db.commit()
    # db.refresh(topic)
    return {"message": "Topic created successfully"}


# This endpoint creates a task handler request. It accepts a JSON body with the details of the task handler (such as crawler_id).
#  It updates the first active task in the database with the provided crawler_id and returns the updated task.
@router.post("/search/username/task/")
def create_task_handler_request(
    task: scheme_task_handler.task_handler, db: session = Depends(get_db)
):
    responses = (
        db.query(models.task_handler_username)
        .filter(models.task_handler_username.is_active == 1)
        .all()
    )

    if responses:
        try:
            result = []
            responses[0].crawler_id = task.crawler_id
            responses[
                0
            ].last_status = f"define task to crwaler number {task.crawler_id}"
            responses[0].is_active = False

            db.commit()

            query = (
                db.query(models.requests_model_search_username)
                .filter(
                    models.requests_model_search_username.task_handler_id
                    == responses[0].id
                )
                .all()
            )

            content_query = (
                db.query(model_get_content.get_content)
                .filter(model_get_content.get_content.id == query[0].content_id)
                .all()
            )

            result.append(
                {
                    "username": query[0].username,
                    "task_handler_id": query[0].task_handler_id,
                    "statistic": content_query[0].statistic,
                    "comments": content_query[0].comments,
                    "description": content_query[0].description,
                    "tags": content_query[0].tags,
                    "quantity": query[0].quantity,
                }
            )

            return result

        except Exception as e:
            print(e)

    else:
        return "no task to do "


# # # a GET endpoint for geting list of the undone topics
@router.get("/search/username/", response_model=list[schemes.get_username])
def get_search_username(db: session = Depends(get_db)):
    get_request = db.query(models.requests_model_search_username).all()
    return get_request


# # a PUT endpoint for marking a topic as done
@router.put("/search/username/{username_id}")
def update_search_username(username_id: int, db: session = Depends(get_db)):
    update_request = (
        db.query(models.requests_model_search_username)
        .filter(models.requests_model_search_username.id == username_id)
        .first()
    )
    if update_request:
        update_request.is_active = False
        db.commit()
        return {"message": "Topic updated successfully"}
    else:
        return {"message": "Topic not found"}


# This endpoint deletes a specific search username task. It accepts an explore_id as a path parameter and deletes the corresponding task from the database.
@router.delete("/search/username/delete/{explore_id}")
def delete_search_username_request(explore_id: int, db: session = Depends(get_db)):
    query = (
        db.query(models.requests_model_search_username)
        .filter(models.requests_model_search_username.id == explore_id)
        .first()
    )
    if query:
        db.delete(query)

        db.commit()
        return "deleted succesfuly"
    else:
        return "no data found "


# This endpoint creates a task handler request for explore tasks. It accepts a JSON body with the details of the task handler (such as crawler_id).
#  It updates the first active explore task in the database with the provided crawler_id and returns the updated task.
# @router.post('/explore/task/')
# def create_task_handler_request(task: scheme_task_handler.task_handler, db: session = Depends(get_db)):

#     responses=db.query(model_explore.task_handler_explore).filter(model_explore.task_handler_explore.is_active==1).all()

#     if responses:
#         try:
#             result=[]
#             responses[0].crawler_id=task.crawler_id
#             responses[0].last_status=f'define task to crwaler number {task.crawler_id}'
#             responses[0].is_active=False

#             db.commit()

#             query= db.query(model_explore.requests_model_explore).filter(model_explore.requests_model_explore.id==responses[0].id).all()
#             content_query=db.query(model_get_content.get_content).filter(model_get_content.get_content.id==query[0].content_id).all()

#             result.append(
#                     {
#                         "category":query[0].category,
#                         "task_handler_id":query[0].task_handler_id,
#                         "statistic":content_query[0].statistic,
#                         "comments":content_query[0].comments,
#                         "description":content_query[0].description,
#                         "tags":content_query[0].tags,
#                         "created_by":query[0].created_by,
#                         "quantity":query[0].quantity

#                     }
#                 )

#             return result
#         except Exception as e :
#             print(e)


#     else:
#         return "no task to do "


# This endpoint accepts a list of responses from the crawler for search username tasks. For each response,
# it updates the corresponding task in the database and inserts the response into a MongoDB collection.
@router.post("/search/username/response/")
def take_response_from_crawler(
    responses: list[scheme_response_username.response_username],
    db: session = Depends(get_db),
):
    if responses:
        result = []

        for response in responses:
            query = (
                db.query(models.task_handler_username)
                .filter(models.task_handler_username.id == response.task_handler_id)
                .all()
            )
            query[
                0
            ].last_status = (
                f"task completed succesfuly by crawler number  {response.crawler_id}"
            )
            query[0].is_done = True
            db.commit()
            result.append({"username": response.username, "content": response.content})

        model_mongo_db.collection.insert_many(result)

        return "ok"

    else:
        query = (
            db.query(models.task_handler_username)
            .filter(models.task_handler_username.id == response.task_handler_id)
            .all()
        )
        query[0].crawler_id = response.crawler_id
        query[
            0
        ].last_status = f"task was failed by crawler number {response.crawler_id}"
        query[0].is_active = True
        db.commit()
        return query
