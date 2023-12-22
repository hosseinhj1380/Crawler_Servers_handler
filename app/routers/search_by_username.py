from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import session
from schemes import (
    scheme_search_username as schemes,
    scheme_task_handler,
    scheme_response_username,
)
from dependencies import get_db
from cruds.username_crud import UsernameCRUD
import base64
from fastapi.responses import JSONResponse

router = APIRouter()


# a POST endpoint for creating a topic
@router.post("/search/username/")
def create_task(username: schemes.search_username, db: session = Depends(get_db)):

    obj = UsernameCRUD(db=db)
    obj.create_task(username=username)

    # db.refresh(topic)
    return {"message": "Topic created successfully"}


# This endpoint creates a task handler request. It accepts a JSON body with the details of the task handler (such as crawler_id).
#  It updates the first active task in the database with the provided crawler_id and returns the updated task.
@router.post("/search/username/task/")
def create_task_handler_request(
    task: scheme_task_handler.task_handler, db: session = Depends(get_db)
):
    obj = UsernameCRUD(db=db)

    query, content_query = obj.create_task_handler_request(task=task)
    try:
        result = []

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
        return JSONResponse(status_code=204, content="not found ")


# # # a GET endpoint for geting list of the undone topics
@router.get("/search/username/", response_model=list[schemes.get_username])
def get_search_username(db: session = Depends(get_db)):

    obj = UsernameCRUD(db=db)

    return obj.get_data()


# # a PUT endpoint for marking a topic as done
@router.put("/search/username/{username_id}")
def update_search_username(username_id: int, db: session = Depends(get_db)):

    obj = UsernameCRUD(db=db)
    return obj.update_data(username_id=username_id)


# This endpoint deletes a specific search username task. It accepts an explore_id as a path parameter and deletes the corresponding task from the database.
@router.delete("/search/username/delete/{username_id}")
def delete_search_username_request(username_id: int, db: session = Depends(get_db)):

    obj = UsernameCRUD(db=db)
    return obj.update_data(username_id=username_id)


# This endpoint accepts a list of responses from the crawler for search username tasks. For each response,
# it updates the corresponding task in the database and inserts the response into a MongoDB collection.
@router.post("/search/username/response/")
def take_response_from_crawler(
    responses: list[scheme_response_username.response_username],
    db: session = Depends(get_db),
):

    result = []
    obj = UsernameCRUD(db=db)

    if responses:

        for response in responses:
            obj.response_handler_success(response=response)

            # for content in response.content:
            #     decoded_video = base64.b64decode(content["video_url"])

            #     with open(f'{content["link"]}.mp4', 'wb') as output_file:
            #         output_file.write(decoded_video)

            #     content["video_url"] = content["link"]

            result.append({"username": response.username,
                          "content": response.content})

        obj.save_mongo(result=result)

        return "responses saved succesfully "

    else:

        return JSONResponse(status_code=400, content="bad request  ")


@router.post("/search/username/response/failed")
def task_response_failed(response: scheme_response_username.ResponseFailed, db: session = (Depends(get_db))):

    obj = UsernameCRUD(db=db)

    return obj.response_handler_failed(responses=response)
