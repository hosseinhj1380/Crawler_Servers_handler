from databases import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship


class RequestModelSearchUsername(Base):
    __tablename__ = "app_requests_model_search_username"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    task_handler_id = Column(Integer, ForeignKey("app_task_handler_username.id"))
    quantity = Column(Integer)

    content_id = Column(Integer, ForeignKey("app_get_content.id"), autoincrement=True)
    content = relationship("GetContent", back_populates="search_username")
    task_handler = relationship(
        "TaskHandlerUsername", back_populates="search_username"
    )


class TaskHandlerUsername(Base):
    __tablename__ = "app_task_handler_username"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean)
    crawler_id = Column(Integer)
    last_status = Column(String)
    is_done = Column(Boolean)

    search_username = relationship(
        "RequestModelSearchUsername", back_populates="task_handler"
    )
