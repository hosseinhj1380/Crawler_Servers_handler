from pydantic import BaseModel


class response_explore(BaseModel):
    crawler_id: int
    task_handler_id: int
    category: str = None
    created_by: str = None

    content: list

    class Config:
        from_attributes = True


# class get_username(search_username):
#     id: int

#     class Config:
#         from_attributes = False
