from pydantic import BaseModel


class search_username(BaseModel):
    statistic: bool = False
    description: bool = False
    comments: bool = False
    tags: bool = False
    username: str = None
    quantity: int = 1

    class Config:
        from_attributes = True


class get_username(search_username):
    id: int

    class Config:
        from_attributes = False
