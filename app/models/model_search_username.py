from databases import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship


class requests_model_search_username(Base):
    __tablename__ = "app_requests_model_search_username"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    task_handler_id = Column(Integer, ForeignKey("app_task_handler_username.id"))
    quantity = Column(Integer)

    content_id = Column(Integer, ForeignKey("app_get_content.id"), autoincrement=True)
    content = relationship("get_content", back_populates="search_username")
    task_handler = relationship(
        "task_handler_username", back_populates="search_username"
    )


class task_handler_username(Base):
    __tablename__ = "app_task_handler_username"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean)
    crawler_id = Column(Integer)
    last_status = Column(String)
    is_done = Column(Boolean)

    search_username = relationship(
        "requests_model_search_username", back_populates="task_handler"
    )
