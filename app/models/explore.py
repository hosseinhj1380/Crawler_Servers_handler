from databases import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

# from .model_get_content import get_content
# from model_get_content import get_content


class RequesModelExplore(Base):
    __tablename__ = "app_requests_model_explore"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    quantity = Column(Integer)
    created_by = Column(String)

    task_handler_id = Column(Integer, ForeignKey("app_task_handler_explore.id"))
    content_id = Column(Integer, ForeignKey("app_get_content.id"))

    get_content = relationship("GetContent", back_populates="explore")
    task_handler = relationship("TaskHandlerExplore", back_populates="explore")


class TaskHandlerExplore(Base):
    __tablename__ = "app_task_handler_explore"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean)
    crawler_id = Column(Integer)
    last_status = Column(String)
    is_done = Column(Boolean)

    explore = relationship("RequesModelExplore", back_populates="task_handler")
