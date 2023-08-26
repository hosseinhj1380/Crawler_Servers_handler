from sqlalchemy.orm import session
from models import model_search_tag as models, model_get_content, model_mongo_db


class CRUDtag:
    def __init__(self, db) -> None:
        self.db = db

    def create_task(self, tag):
        new_content_request = model_get_content.GetContent(
            statistic=tag.statistic,
            description=tag.description,
            comments=tag.comments,
            tags=tag.tags,
        )

        task_handler = models.TaskHandlerTag(
            is_active=True, last_status="define task ", is_done=False, crawler_id=0
        )

        new_search_tag = models.RequestModelSearchTag(
            title=tag.title,
            quantity=tag.quantity,
            content=new_content_request,
            task_handler=task_handler,
        )
        self.db.add(new_search_tag)
        self.db.commit()

    def create_task_handler(self, task):

        responses = (
            self.db.query(models.TaskHandlerTag)
            .filter(models.TaskHandlerTag.is_active == True)
            .all()
        )
        if responses:
            responses[0].crawler_id = task.crawler_id
            responses[0].last_status = f"define task to crwaler number {task.crawler_id}"
            responses[0].is_active = False

            self.db.commit()

            query = (
                self.db.query(models.RequestModelSearchTag)
                .filter(
                    models.RequestModelSearchTag.task_handler_id == responses[0].id
                )
                .all()
            )
            content_query = (
                self.db.query(model_get_content.GetContent)
                .filter(model_get_content.GetContent.id == query[0].content_id)
                .all()
            )
            return (query, content_query)

    def get_data(self):

        return self.db.query(models.RequestModelSearchTag).all()

    def update_data(self, tag_id):

        update_query = (
            self.db.query(models.RequestModelSearchTag)
            .filter(models.RequestModelSearchTag.id == tag_id)
            .first()
        )
        if update_query:
            update_query.is_active = False
            self.db.commit()
            return {"message": "Order updated successfully"}
        else:
            return {"message": "Order not found"}

    def delete_data(self, tag_id):
        query = (
            self.db.query(models.RequestModelSearchTag)
            .filter(models.RequestModelSearchTag.id == tag_id)
            .first()
        )
        if query:
            self.db.delete(query)

            self.db.commit()
            return "deleted succesfuly"
        else:
            return "no data found "

    def response_handler_success(self, response):
        query = (
            self.db.query(models.TaskHandlerTag)
            .filter(models.TaskHandlerTag.id == response.task_handler_id)
            .all()
        )
        query[
            0
        ].last_status = (
            f"task completed succesfuly by crawler number  {response.crawler_id}"
        )
        query[0].is_done = True
        self.db.commit()

    def response_handler_failed(self, responses):
        query = (
            self.db.query(models.TaskHandlerTag)
            .filter(models.TaskHandlerTag.id == responses.task_handler_id)
            .all()
        )
        if query[0].crawler_id == responses.crawler_id:
            query[0].last_status = f"task was failed by crawler number {responses.crawler_id} because {responses.reason}"
            query[0].is_active = True
            self.db.commit()
        return "success "

    def save_mongo(self, result):
        model_mongo_db.collection.insert_many(result)
