from pydantic import BaseModel


class response_username(BaseModel):
    username: str
    crawler_id: int
    task_handler_id: int
    content: list

    class Config:
        from_attributes = True

class ResponseFailed(BaseModel):
    crawler_id: int
    task_handler_id: int
    reason:str