from sqlalchemy import Column, Integer, String,ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    id_department = Column(Integer, ForeignKey("departament.id"))
    name = Column(String)

    department = relationship("Departament", back_populates="cities")