from pydantic import BaseModel


class task_handler(BaseModel):
    crawler_id: int = 0
    # last_status:str
    # is_done:bool=False

    class Config:
        from_attributes = True


# class get_username(search_username):
#     id: int

#     class Config:
#         from_attributes = False
