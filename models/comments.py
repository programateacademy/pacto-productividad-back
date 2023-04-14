from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    id_post= Column(Integer, ForeignKey("posts.id"))
    status = Column(Integer)
    description = Column(String)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    post_owner= relationship("Posts", back_populates="comments")
    
