from sqlalchemy import Column, Integer,ForeignKey,String,Text
from database import Base
from sqlalchemy.orm import relationship

class TextContribution(Base):
    __tablename__ = 'text_contribution'

    id = Column(Integer, primary_key=True, index=True)
    contribution_id = Column(Integer, ForeignKey('contribution.id'))
    contribution_text = Column(Text, nullable=True)

    contribution = relationship('Contribution', back_populates='text_contributions')