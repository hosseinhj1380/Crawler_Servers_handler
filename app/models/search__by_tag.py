from databases import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship


class RequestModelSearchTag(Base):
    __tablename__ = "app_requests_model_search_tag"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    task_handler_id = Column(Integer, ForeignKey("app_task_handler_tag.id"))

    quantity = Column(Integer)
    content_id = Column(Integer, ForeignKey("app_get_content.id"))

    content = relationship("GetContent", back_populates="search_tag")
    task_handler = relationship("TaskHandlerTag", back_populates="search_tag")


class TaskHandlerTag(Base):
    __tablename__ = "app_task_handler_tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean)
    crawler_id = Column(Integer)
    last_status = Column(String)
    is_done = Column(Boolean)

    search_tag = relationship(
        "RequestModelSearchTag", back_populates="task_handler"
    )
