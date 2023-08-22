from databases import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship


class get_content(Base):
    __tablename__ = "app_get_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    statistic = Column(Boolean)
    description = Column(Boolean)
    comments = Column(Boolean)
    tags = Column(Boolean)
    # is_active=Column(Boolean)
    explore = relationship("requests_model_explore", back_populates="get_content")
    search_tag = relationship("requests_model_search_tag", back_populates="content")
    search_username = relationship(
        "requests_model_search_username", back_populates="content"
    )
