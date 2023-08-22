# from databases import Base
# from sqlalchemy import Column, Integer, Boolean,String,ForeignKey
# from sqlalchemy.orm import relationship


# class task_handler(Base):

#     __tablename__ = 'app_task_handler'
#     id = Column(Integer, primary_key=True,autoincrement=True)
#     is_active=Column(Boolean)
#     crawler_id=Column(Integer)
#     last_status=Column(String)
#     is_done=Column(Boolean)


#     explore_id=Column(Integer,ForeignKey("app_requests_model_explore.id"))
#     # search_tag_id=Column(Integer,ForeignKey("app_requests_model_search_tag.id"))
#     # search_username_id=Column(Integer,ForeignKey("app_requests_model_search_username.id"))

#     explore=relationship('requests_model_explore',back_populates='task_handler')
#     # search_tag=relationship('app_requests_model_search_tag',back_populates='task_handler')
#     # search_username=relationship('app_requests_model_search_username',back_populates='task_handler')
