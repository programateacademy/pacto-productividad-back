from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy.orm import relationship


class TypeActor(Base):
    __tablename__ = "type_actor"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Integer)
    type_actor = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user_TA= relationship("Users", back_populates="type_actor_U")
