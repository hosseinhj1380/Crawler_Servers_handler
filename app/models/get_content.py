from databases import Base
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship


class GetContent(Base):
    __tablename__ = "app_get_content"

    id = Column(Integer, primary_key=True, autoincrement=True)
    statistic = Column(Boolean)
    description = Column(Boolean)
    comments = Column(Boolean)
    tags = Column(Boolean)
    # is_active=Column(Boolean)
    explore = relationship("RequesModelExplore", back_populates="get_content")
    search_tag = relationship("RequestModelSearchTag", back_populates="content")
    search_username = relationship(
        "RequestModelSearchUsername", back_populates="content"
    )
