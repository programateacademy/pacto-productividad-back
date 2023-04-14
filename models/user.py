from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime,ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Users(Base):
    __tablename__ = "users"

    # Columns definition
    id = Column(Integer, primary_key=True, index=True) # Unique identifier for each user
    id_type_actor= Column(Integer, ForeignKey("type_actor.id")) # Foreign key to reference the type of actor of the user
    id_city = Column(Integer, ForeignKey("city.id")) # Foreign key to reference the city of the user
    id_contribution= Column(Integer, ForeignKey("contribution.id")) # Foreign key to reference the contribution of the user
    name_user = Column(String) # First name of the user
    lastname = Column(String) # Last name of the user
    email = Column(String) # Email address of the user
    username = Column(String) # Username of the user
    password = Column(String) # Hashed password of the user
    hashed_password = Column(String) # Hashed password of the user (deprecated)
    cohabitation_agreement = Column(Boolean) # Boolean indicating if the user has a cohabitation agreement
    name_enti = Column(String) #
    contribution_text = Column(Text, nullable=True)
    type_user = Column(Integer, default=0) # Status of the user (e.g. active, inactive)
    status = Column(Integer, default=0) # Status of the user (e.g. active, inactive)
    description = Column(Text) # Description of the user (bio, summary, etc.)
    knowledge_interests = Column(Text) # User's interests or areas of knowledge
    created_at = Column(DateTime) # Date and time of creation of the user's account
    updated_at = Column(DateTime) # Date and time of the last update to the user's account
    forgot_password = Column(Boolean) # Boolean indicating if the user forgot their password
    image_profile = Column(String) # URL or path to the user's profile picture
    phone_number = Column(String) # Phone number of the user

    # Relationship with the Posts table
    posts = relationship("Posts", back_populates="owner")

    # Relationship with the TypeActor table
    type_actor_U = relationship("TypeActor", back_populates="user_TA")

    # Relationship with the Contribution table
    contribution = relationship('Contribution', back_populates='users')