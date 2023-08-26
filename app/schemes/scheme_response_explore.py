from pydantic import BaseModel
from typing import List


class response_explore(BaseModel):
    crawler_id: int
    task_handler_id: int
    category: str = None
    created_by: str = None


    content: List[dict]

    class Config:
        from_attributes = True


class ResponseFailed(BaseModel):
    crawler_id: int
    task_handler_id: int
    reason:str

# class get_username(search_username):
#     id: int

#     class Config:
#         from_attributes = False
