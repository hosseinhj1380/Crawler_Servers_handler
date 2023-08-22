import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import uvicorn
from .model import collection

from typing import List

app = FastAPI()


@strawberry.type
class Comments:
    main_comment: str
    sub_comment: str


@strawberry.type
class Statistic:
    likes_number: int
    saved_number: int
    shared_number: int
    comments_number: int


@strawberry.type
class Content:
    username: str
    link: str
    description: str
    statistics: List[Statistic]
    comments: list[Comments]
    tags: List[str]
    post_date: str
    video_url: str


# Define your GraphQL schema using Strawberry
@strawberry.type
class Query:
    @strawberry.field
    def explore(self, category: str = None, created_by: str = None) -> List[Content]:
        if category is not None and created_by is None:
            items = collection.find({"category": category})
        elif category is None and created_by is not None:
            items = collection.find({"created_by": created_by})
        else:
            items = collection.find({"category": category, "created_by": created_by})

        result = []
        for item in items:
            result.append(
                Content(
                    username=item["content"][0]["username"],
                    link=item["content"][0]["link"],
                    description=item["content"][0]["description"],
                    post_date=item["content"][0]["post_date"],
                    video_url=item["content"][0]["video_url"],
                    tags=item["content"][0]["tags"],
                    comments=[
                        Comments(
                            main_comment=comment["main_comment"],
                            sub_comment=comment["sub_comment"],
                        )
                        for comment in item["content"][0]["comments"]
                    ],
                    statistics=[
                        Statistic(
                            likes_number=item["content"][0]["statistic"][0][
                                "likes_number"
                            ],
                            saved_number=item["content"][0]["statistic"][0][
                                "saved_number"
                            ],
                            shared_number=item["content"][0]["statistic"][0][
                                "shared_number"
                            ],
                            comments_number=item["content"][0]["statistic"][0][
                                "comments_number"
                            ],
                        )
                    ],
                )
            )
        return result

    @strawberry.field
    def search_tag(self, tag: str = "nothing") -> List[Content]:
        items = collection.find({"title": tag})
        result = []
        for item in items:
            result.append(
                Content(
                    username=item["content"][0]["username"],
                    link=item["content"][0]["link"],
                    description=item["content"][0]["description"],
                    post_date=item["content"][0]["post_date"],
                    video_url=item["content"][0]["video_url"],
                    tags=item["content"][0]["tags"],
                    comments=[
                        Comments(
                            main_comment=comment["main_comment"],
                            sub_comment=comment["sub_comment"],
                        )
                        for comment in item["content"][0]["comments"]
                    ],
                    statistics=[
                        Statistic(
                            likes_number=item["content"][0]["statistic"][0][
                                "likes_number"
                            ],
                            saved_number=item["content"][0]["statistic"][0][
                                "saved_number"
                            ],
                            shared_number=item["content"][0]["statistic"][0][
                                "shared_number"
                            ],
                            comments_number=item["content"][0]["statistic"][0][
                                "comments_number"
                            ],
                        )
                    ],
                )
            )
        return result

    @strawberry.field
    def search_username(self, username: str = "nothing") -> List[Content]:
        items = collection.find({"username": username})
        result = []
        for item in items:
            result.append(
                Content(
                    username=item["content"][0]["username"],
                    link=item["content"][0]["link"],
                    description=item["content"][0]["description"],
                    post_date=item["content"][0]["post_date"],
                    video_url=item["content"][0]["video_url"],
                    tags=item["content"][0]["tags"],
                    comments=[
                        Comments(
                            main_comment=comment["main_comment"],
                            sub_comment=comment["sub_comment"],
                        )
                        for comment in item["content"][0]["comments"]
                    ],
                    statistics=[
                        Statistic(
                            likes_number=item["content"][0]["statistic"][0][
                                "likes_number"
                            ],
                            saved_number=item["content"][0]["statistic"][0][
                                "saved_number"
                            ],
                            shared_number=item["content"][0]["statistic"][0][
                                "shared_number"
                            ],
                            comments_number=item["content"][0]["statistic"][0][
                                "comments_number"
                            ],
                        )
                    ],
                )
            )
        return result


# Create the GraphQL app using the schema and FastAPI
graphql_app = GraphQL(schema=strawberry.Schema(query=Query))

# Mount the GraphQL app to the FastAPI app
app.add_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7000)
