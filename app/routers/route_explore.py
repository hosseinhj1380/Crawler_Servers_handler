from fastapi import Depends, APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import session
from schemes import schemes_explore as schemes, scheme_response_explore
from schemes import scheme_task_handler
from models import model_explore, model_get_content, model_mongo_db
from dependencies import get_db


router = APIRouter()


# a POST endpoint for creating a explore task


@router.post(
    "/explore/",
    summary="create a explore task ",
    description="this is an endpoint to create new task for crawler ",
)
def create_explore_request(explore: schemes.explore, db: session = Depends(get_db)):
    new_content_request = model_get_content.get_content(
        statistic=explore.statistic,
        description=explore.description,
        comments=explore.comments,
        tags=explore.tags,
    )
    task_handler = model_explore.task_handler_explore(
        is_active=True, last_status="define task ", is_done=False, crawler_id=0
    )
    new_request = model_explore.requests_model_explore(
        category=explore.category,
        quantity=explore.quantity,
        created_by=explore.created_by,
        get_content=new_content_request,
        task_handler=task_handler,
    )

    db.add(new_request)
    db.commit()
    # db.refresh(explore)
    return {"message": "explore request created successfully"}


# This endpoint creates a task handler request.
# It accepts a JSON body with the details of the task handler (such as crawler_id).
# It updates the first active task in the database with the provided crawler_id and returns the updated task.
@router.post("/explore/task/")
def create_task_handler_request(
    task: scheme_task_handler.task_handler, db: session = Depends(get_db)
):
    responses = (
        db.query(model_explore.task_handler_explore)
        .filter(model_explore.task_handler_explore.is_active == 1)
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
                db.query(model_explore.requests_model_explore)
                .filter(
                    model_explore.requests_model_explore.task_handler_id
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
                    "category": query[0].category,
                    "task_handler_id": query[0].task_handler_id,
                    "statistic": content_query[0].statistic,
                    "comments": content_query[0].comments,
                    "description": content_query[0].description,
                    "tags": content_query[0].tags,
                    "created_by": query[0].created_by,
                    "quantity": query[0].quantity,
                }
            )

            return result

        except Exception as e:
            print(e)

    else:
        return JSONResponse(status_code=204, content=None)


# This endpoint accepts a list of responses from the crawler. For each response,
# it updates the corresponding task in the database and inserts the response into a MongoDB collection.
@router.post("/explore/response/")
def take_response_from_crawler(
    responses: list[scheme_response_explore.response_explore],
    db: session = Depends(get_db),
):
    if responses:
        result = []

        for response in responses:
            query = (
                db.query(model_explore.task_handler_explore)
                .filter(
                    model_explore.task_handler_explore.id == response.task_handler_id
                )
                .all()
            )
            query[
                0
            ].last_status = (
                f"task completed succesfuly by crawler number  {response.crawler_id}"
            )
            query[0].is_done = True
            db.commit()
            result.append(
                {
                    "category": response.category,
                    "created_by": response.created_by,
                    "content": response.content,
                }
            )

        model_mongo_db.collection.insert_many(result)

        return "ok"

    else:
        query = (
            db.query(model_explore.task_handler_explore)
            .filter(model_explore.task_handler_explore.id == response.task_handler_id)
            .all()
        )
        query[0].crawler_id = response.crawler_id
        query[
            0
        ].last_status = f"task was failed by crawler number {response.crawler_id}"
        query[0].is_active = True
        db.commit()
        return query


# a GET endpoint for geting list of the undone explore task
@router.get("/explore/", response_model=list[schemes.explore_get])
def get_explore_request(db: session = Depends(get_db)):
    result = db.query(model_explore.requests_model_explore).all()
    return result


# a PUT endpoint for marking a explore task  as done
@router.put("/explore/{explore_id}")
def update_explore(explore_id: int, db: session = Depends(get_db)):
    update_data = (
        db.query(model_explore.requests_model_explore)
        .filter(model_explore.requests_model_explore.id == explore_id)
        .first()
    )

    if update_data:
        update_data.is_active = 0
        db.commit()
        return {"message": "explore updated successfully"}
    else:
        return {
            "message": "explore not found",
        }


# This endpoint deletes a specific explore task. It accepts an explore_id as a path parameter and deletes the corresponding task from the database.
@router.delete("/explore/delete/{explore_id}")
def delete_explore_request(explore_id: int, db: session = Depends(get_db)):
    query = (
        db.query(model_explore.requests_model_explore)
        .filter(model_explore.requests_model_explore.id == explore_id)
        .first()
    )
    if query:
        db.delete(query)

        db.commit()
        return "deleted succesfuly"
    else:
        return "no data found "


@router.post("/test/")
def create_comment(
    comment_id: int = Query(
        None,
        title="title text",
        description="Description Text !",
        alias="CommentID",
        deprecated=True,
    )
):
    return {"comment_id": comment_id}
