from pydantic import BaseModel


class explore(BaseModel):
    statistic: bool = False
    comments: bool = False
    description: bool = False
    tags: bool = False
    # is_active:bool
    category: str = "Dance and Music"
    quantity: int = 1
    created_by: str = None

    class Config:
        from_attributes = True


class explore_get(explore):
    id: int

    class Config:
        from_attributes = True
