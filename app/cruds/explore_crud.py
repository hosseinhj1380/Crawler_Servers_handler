from sqlalchemy.orm import session
from app.models import explore, get_content
from app.models import mongo_db


class CRUDexplore:

    def __init__(self, db) -> None:

        self.db = db

    def create_task(self, explore):

        new_content_request = get_content.GetContent(
            statistic=explore.statistic,
            description=explore.description,
            comments=explore.comments,
            tags=explore.tags)

        task_handler = explore.TaskHandlerExplore(
            is_active=True, last_status="define task ", is_done=False, crawler_id=0)

        new_request = explore.RequesModelExplore(
            category=explore.category,
            quantity=explore.quantity,
            created_by=explore.created_by,
            get_content=new_content_request,
            task_handler=task_handler,)

        self.db.add(new_request)
        self.db.commit()
        self.db.refresh(new_request)

    def create_task_handler(self, task):

        responses = (
            self.db.query(explore.TaskHandlerExplore)
            .filter(explore.TaskHandlerExplore.is_active == True)
            .all())
        if responses:

            responses[0].crawler_id = task.crawler_id
            responses[0].last_status = f"define task to crwaler number {task.crawler_id}"
            responses[0].is_active = False

            self.db.commit()

            query = (
                self.db.query(explore.RequesModelExplore)
                .filter(
                    explore.RequesModelExplore.task_handler_id
                    == responses[0].id
                )
                .all()
            )
            content_query = (
                self.db.query(get_content.GetContent)
                .filter(get_content.GetContent.id == query[0].content_id)
                .all()
            )

            return (query, content_query)

    def response_handler_success(self, response):
        query = (
            self.db.query(explore.TaskHandlerExplore)
            .filter(
                explore.TaskHandlerExplore.id == response.task_handler_id
            )
            .all()
        )
        query[0].last_status = (
            f"task completed succesfuly by crawler number  {response.crawler_id}"
        )
        query[0].is_done = True
        self.db.commit()

    def response_handler_failed(self, responses):
        query = (
            self.db.query(explore.TaskHandlerExplore)
            .filter(explore.TaskHandlerExplore.id == responses.task_handler_id)
            .all()
        )
        if query[0].crawler_id == responses.crawler_id:
            query[0].last_status = f"task was failed by crawler number {responses.crawler_id}because {responses.reason}"
            query[0].is_active = True
            self.db.commit()
        return "success "

    def save_mongo(self, result):

        mongo_db.collection.insert_many(result)

    def get_data(self):
        return self.db.query(explore.RequesModelExplore).all()

    def put_data(self, explore_id):

        update_data = (self.db.query(explore.RequesModelExplore)
                       .filter(explore.RequesModelExplore.id == explore_id)
                       .first())
        if update_data:
            update_data.is_active = False
            self.db.commit()
            return {"message": "explore updated successfully"}
        else:
            return {
                "message": "explore not found",
            }

    def delete_data(self, explore_id):
        query = (
            self.db.query(explore.RequesModelExplore)
            .filter(explore.RequesModelExplore.id == explore_id)
            .first()
        )
        if query:
            self.db.delete(query)
            self.db.commit()

            return "deleted succesfuly"
        else:
            return "no data found "

    # def task_response_feiled(self,response):

    #     query=
