from databases import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship


class requests_model_search_tag(Base):
    __tablename__ = "app_requests_model_search_tag"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    task_handler_id = Column(Integer, ForeignKey("app_task_handler_tag.id"))

    quantity = Column(Integer)
    content_id = Column(Integer, ForeignKey("app_get_content.id"))

    content = relationship("get_content", back_populates="search_tag")
    task_handler = relationship("task_handler_tag", back_populates="search_tag")


class task_handler_tag(Base):
    __tablename__ = "app_task_handler_tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean)
    crawler_id = Column(Integer)
    last_status = Column(String)
    is_done = Column(Boolean)

    search_tag = relationship(
        "requests_model_search_tag", back_populates="task_handler"
    )
