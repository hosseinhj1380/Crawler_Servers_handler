from pydantic import BaseModel


class search_tag(BaseModel):
    statistic: bool = False
    description: bool = False
    comments: bool = False
    tags: bool = False
    title: str = None
    quantity: int = 0

    # class Config:
    #     from_attributes = True


class get_tag(search_tag):
    id: int

    # class Config:
    #     from_attributes = False
