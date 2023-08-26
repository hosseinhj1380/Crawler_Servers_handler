from models import model_search_username as models, model_get_content, model_mongo_db


class UsernameCRUD:
    def __init__(self, db) -> None:
        self.db = db

    def create_task(self, username):
        new_content_request = model_get_content.GetContent(
            statistic=username.statistic,
            description=username.description,
            comments=username.comments,
            tags=username.tags,
        )
        task_handler = models.TaskHandlerUsername(
            is_active=True, last_status="create task ", is_done=False, crawler_id=0
        )

        new_request = models.RequestModelSearchUsername(
            username=username.username,
            quantity=username.quantity,
            content=new_content_request,
            task_handler=task_handler,
        )
        self.db.add(new_request)
        self.db.commit()

    def create_task_handler_request(self, task):

        responses = (
            self.db.query(models.TaskHandlerUsername)
            .filter(models.TaskHandlerUsername.is_active == True)
            .all()
        )

        if responses:

            responses[0].crawler_id = task.crawler_id
            responses[0].last_status = f"define task to crwaler number {task.crawler_id}"
            responses[0].is_active = False

            self.db.commit()

            query = (
                self.db.query(models.RequestModelSearchUsername)
                .filter(
                    models.RequestModelSearchUsername.task_handler_id == responses[0].id
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
        return self.db.query(models.RequestModelSearchUsername).all()

    def update_data(self, username_id):
        update_request = (
            self.db.query(models.RequestModelSearchUsername)
            .filter(models.RequestModelSearchUsername.id == username_id)
            .first()
        )
        if update_request:
            update_request.is_active = False
            self.db.commit()
            return {"message": "Topic updated successfully"}
        else:
            return {"message": "Topic not found"}

    def delete_data(self, username_id):
        query = (
            self.db.query(models.RequestModelSearchUsername)
            .filter(models.RequestModelSearchUsername.id == username_id)
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
            self.db.query(models.TaskHandlerUsername)
            .filter(models.TaskHandlerUsername.id == response.task_handler_id)
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
            self.db.query(models.TaskHandlerUsername)
            .filter(models.TaskHandlerUsername.id == responses.task_handler_id)
            .all()
        )
        if query[0].crawler_id == responses.crawler_id:
            query[0].last_status = f"task was failed by crawler number {responses.crawler_id}because {responses.reason}"
            query[0].is_active = True
            self.db.commit()
        return "success "

    def save_mongo(self, result):
        model_mongo_db.collection.insert_many(result)
