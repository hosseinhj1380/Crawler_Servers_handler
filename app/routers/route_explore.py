from fastapi import Depends, APIRouter, Query, File, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import session
from schemes import schemes_explore as schemes, scheme_response_explore
from schemes import scheme_task_handler

from dependencies import get_db
from typing import List
import base64
from cruds.explore_crud import CRUDexplore


router = APIRouter()


# a POST endpoint for creating a explore task


@router.post(
    "/explore/",
    summary="create a explore task ",
    description="this is an endpoint to create new task for crawler ",
)
def create_explore_request(explore: schemes.explore, db: session = Depends(get_db)):

    obj = CRUDexplore(db=db)
    obj.create_task(explore=explore)

    return {"message": "explore request created successfully"}


# This endpoint creates a task handler request.
# It accepts a JSON body with the details of the task handler (such as crawler_id).
# It updates the first active task in the database with the provided crawler_id and returns the updated task.
@router.post("/explore/task/")
def create_task_handler_request(
    task: scheme_task_handler.task_handler, db: session = Depends(get_db)
):
    obj = CRUDexplore(db=db)

    try:

        query, content_query = obj.create_task_handler(task=task)

        result = []
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
        return JSONResponse(status_code=204, content="not found ")


# This endpoint accepts a list of responses from the crawler. For each response,
# it updates the corresponding task in the database and inserts the response into a MongoDB collection.
@router.post("/explore/response/")
def take_response_from_crawler(
    responses: list[scheme_response_explore.response_explore],
    db: session = Depends(get_db),
):
    obj = CRUDexplore(db=db)
    if responses:

        result = []
        for response in responses:

            obj.response_handler_success(response=response)

            # for content in response.content:
            #     decoded_video = base64.b64decode(content["video_url"])

            #     with open(f'{content["link"]}.mp4', 'wb') as output_file:
            #         output_file.write(decoded_video)

            #     content["video_url"] = content["link"]

            result.append(
                {
                    "category": response.category,
                    "created_by": response.created_by,
                    "content": response.content,
                }
            )

            obj.save_mongo(result=result)

        return "responses saved succesfully "

    else:
        return JSONResponse(status_code=400, content="bad request  ")


# a GET endpoint for geting list of the undone explore task
@router.get("/explore/", response_model=list[schemes.explore_get])
def get_explore_request(db: session = Depends(get_db)):
    obj = CRUDexplore(db=db)

    return obj.get_data()


# a PUT endpoint for marking a explore task  as done
@router.put("/explore/{explore_id}")
def update_explore(explore_id: int, db: session = Depends(get_db)):

    obj = CRUDexplore(db=db)
    result = obj.put_data(explore_id=explore_id)
    return result


# This endpoint deletes a specific explore task. It accepts an explore_id as a path parameter and deletes the corresponding task from the database.
@router.delete("/explore/delete/{explore_id}")
def delete_explore_request(explore_id: int, db: session = Depends(get_db)):

    obj = CRUDexplore(db=db)

    return obj.delete_data(explore_id=explore_id)


@router.post("/explore/response/failed")
def task_response_failed(response: scheme_response_explore.ResponseFailed, db: session = (Depends(get_db))):

    obj = CRUDexplore(db=db)

    return obj.response_handler_failed(responses=response)


# @router.post("/upload/")
# def upload_videos(files: List[UploadFile] = File(...)):
#     try:
#         for file in files:
#             # Process each uploaded video file here (e.g., save to disk, analyze, etc.)
#             # You can access the uploaded video's contents using `file.file`.
#             # Replace the following line with your processing logic.
#             # For now, let's just print the file name.
#             print("Uploaded file:", file.filename)

#         return JSONResponse(content={"message": "Video(s) uploaded successfully"})
#     except Exception as e:
#         return JSONResponse(content={"message": "An error occurred", "error": str(e)}, status_code=500)
