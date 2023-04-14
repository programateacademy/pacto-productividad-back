from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    id_user= Column(Integer, ForeignKey("users.id"))
    status = Column(Integer)
    description = Column(String)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    image_post = Column(String)
    document_post = Column(String)
    video_post = Column(String)

    owner= relationship("Users", back_populates="posts")

    comments= relationship("Comments", back_populates="post_owner")



