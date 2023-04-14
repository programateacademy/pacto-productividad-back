from sqlalchemy import Column, Integer,ForeignKey, String
from database import Base
from sqlalchemy.orm import relationship
from models.contribution_text import TextContribution


class Contribution(Base):
    __tablename__ = 'contribution'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    users = relationship('Users', back_populates='contribution')
    
    text_contributions = relationship('TextContribution', back_populates='contribution')