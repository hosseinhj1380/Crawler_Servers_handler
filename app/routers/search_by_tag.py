from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import session
from schemes import (
    scheme_search_tag as schemes,
    scheme_task_handler,
    scheme_response_tag,
)

from dependencies import get_db
import base64
from cruds.tag_crud import CRUDtag
from fastapi.responses import JSONResponse


router = APIRouter()


# a POST endpoint for creating a main page order
@router.post("/search/tag/")
def create_main_page_order(tag: schemes.search_tag, db: session = Depends(get_db)):
    obj = CRUDtag(db=db)
    obj.create_task(tag=tag)
    # db.refresh(newnew_search_tag_order)
    return {"message": "request created successfully"}


# This endpoint accepts a JSON body with the details of the task handler (such as crawler_id).
# It fetches the first active task from the database and updates it with the provided crawler_id. It then commits the changes to the database.
@router.post("/search/tag/task/")
def create_task_handler_request(
    task: scheme_task_handler.task_handler, db: session = Depends(get_db)
):
    obj = CRUDtag(db=db)

    try:
        query, content_query = obj.create_task_handler(task=task)
        result = []

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
        return "no task to do "


# a GET endpoint for geting list of the undone orders
@router.get("/search/tag/", response_model=list[schemes.get_tag])
def get_search_by_tag(db: session = Depends(get_db)):
    obj = CRUDtag(db=db)
    return obj.get_data()


# a PUT endpoint for marking an order as done
@router.put("/search/tag/{tag_id}")
def update_tag_request(tag_id: int, db: session = Depends(get_db)):
    obj = CRUDtag(db=db)

    return obj.update_data(tag_id=tag_id)


# This endpoint deletes a specific search tag task. It accepts an explore_id as a path parameter, fetches the corresponding task from the database, and deletes it. If the task is successfully deleted,
#  it commits the changes to the database and returns a success message. If the task is not found, it returns a "no data found" message.
@router.delete("/search/tag/delete/{tag_id}")
def delete_explore_request(tag_id: int, db: session = Depends(get_db)):
    obj = CRUDtag(db=db)
    return obj.delete_data(tag_id=tag_id)


# this endpoint accepts a list of responses from the crawler for search tag tasks. For each response
@router.post("/search/tag/response/")
def take_response_from_crawler(
    responses: list[scheme_response_tag.response_tag], db: session = Depends(get_db)
):

    obj = CRUDtag(db=db)

    if responses:
        result = []

        for response in responses:

            obj.response_handler_success(response=response)
            # for content in response.content:
            #     decoded_video = base64.b64decode(content["video_url"])

            #     with open(f'{content["link"]}.mp4', 'wb') as output_file:
            #         output_file.write(decoded_video)

            #     content["video_url"] = content["link"]
            result.append({"title": response.title,
                          "content": response.content})

        obj.save_mongo(result=result)

        return "responses saved succesfully "

    else:

        return JSONResponse(status_code=400, content="bad request  ")


@router.post("/search/tag/response/failed")
def task_response_failed(response: scheme_response_tag.ResponseFailed, db: session = (Depends(get_db))):

    obj = CRUDtag(db=db)

    return obj.response_handler_failed(responses=response)
