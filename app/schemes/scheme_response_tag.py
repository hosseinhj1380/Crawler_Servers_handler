from pydantic import BaseModel


class response_tag(BaseModel):
    title: str
    crawler_id: int
    task_handler_id: int
    content: list

    class Config:
        from_attributes = True
