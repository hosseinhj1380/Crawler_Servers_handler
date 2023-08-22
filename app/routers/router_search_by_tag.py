from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import session
from schemes import (
    scheme_search_tag as schemes,
    scheme_task_handler,
    scheme_response_tag,
)
from models import model_search_tag as models, model_get_content, model_mongo_db
from dependencies import get_db


router = APIRouter()


# a POST endpoint for creating a main page order
@router.post("/search/tag/")
def create_main_page_order(tag: schemes.search_tag, db: session = Depends(get_db)):
    new_content_request = model_get_content.get_content(
        statistic=tag.statistic,
        description=tag.description,
        comments=tag.comments,
        tags=tag.tags,
    )

    task_handler = models.task_handler_tag(
        is_active=True, last_status="define task ", is_done=False, crawler_id=0
    )

    new_search_tag = models.requests_model_search_tag(
        title=tag.title,
        quantity=tag.quantity,
        content=new_content_request,
        task_handler=task_handler,
    )
    db.add(new_search_tag)
    db.commit()
    # db.refresh(newnew_search_tag_order)
    return {"message": "request created successfully"}


# This endpoint accepts a JSON body with the details of the task handler (such as crawler_id).
# It fetches the first active task from the database and updates it with the provided crawler_id. It then commits the changes to the database.
@router.post("/search/tag/task/")
def create_task_handler_request(
    task: scheme_task_handler.task_handler, db: session = Depends(get_db)
):
    responses = (
        db.query(models.task_handler_tag)
        .filter(models.task_handler_tag.is_active == 1)
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
                db.query(models.requests_model_search_tag)
                .filter(
                    models.requests_model_search_tag.task_handler_id == responses[0].id
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
                    "title": query[0].title,
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
            return e

    else:
        return "no task to do "


# a GET endpoint for geting list of the undone orders
@router.get("/search/tag/", response_model=list[schemes.get_tag])
def get_search_by_tag(db: session = Depends(get_db)):
    Query = db.query(models.requests_model_search_tag).all()
    return Query


# a PUT endpoint for marking an order as done
@router.put("/search/tag/{tag_id}")
def update_tag_request(tag_id: int, db: session = Depends(get_db)):
    update_query = (
        db.query(models.requests_model_search_tag)
        .filter(models.requests_model_search_tag.id == tag_id)
        .first()
    )
    if update_query:
        update_query.is_active = 0
        db.commit()
        return {"message": "Order updated successfully"}
    else:
        return {"message": "Order not found"}


# This endpoint deletes a specific search tag task. It accepts an explore_id as a path parameter, fetches the corresponding task from the database, and deletes it. If the task is successfully deleted,
#  it commits the changes to the database and returns a success message. If the task is not found, it returns a "no data found" message.
@router.delete("/search/tag/delete/{explore_id}")
def delete_explore_request(explore_id: int, db: session = Depends(get_db)):
    query = (
        db.query(models.requests_model_search_tag)
        .filter(models.requests_model_search_tag.id == explore_id)
        .first()
    )
    if query:
        db.delete(query)

        db.commit()
        return "deleted succesfuly"
    else:
        return "no data found "


# this endpoint accepts a list of responses from the crawler for search tag tasks. For each response
@router.post("/search/tag/response/")
def take_response_from_crawler(
    responses: list[scheme_response_tag.response_tag], db: session = Depends(get_db)
):
    if responses:
        result = []

        for response in responses:
            query = (
                db.query(models.task_handler_tag)
                .filter(models.task_handler_tag.id == response.task_handler_id)
                .all()
            )
            query[
                0
            ].last_status = (
                f"task completed succesfuly by crawler number  {response.crawler_id}"
            )
            query[0].is_done = True
            db.commit()
            result.append({"title": response.title, "content": response.content})

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
