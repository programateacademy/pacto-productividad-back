from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.contribution_text import TextContribution as ContributiontextModel
from schemas.contribution_text import ContributionText as ContributiontextSchema

class contributiontextService():
    def __init__(self, db: Session):
        if not isinstance(db, Session):
            raise TypeError("db must be a Session instance")
        self.db = db

    @staticmethod
    def get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()

    def get_contributiontext(self):
        result = self.db.query(ContributiontextModel).all()
        return result
    
    def create_contributiontext(self, contributiontext:ContributiontextModel):
        # current_user = ServiceToken.get_current_active_userid()
        contributiontext_model = ContributiontextModel(
        contribution_id= contributiontext.contribution_id,
        contribution_text = contributiontext.contribution_text
        )
        self.db.add(contributiontext_model)
        self.db.commit()
        return
    
    def get_contributiontext_by_id(self,id:int):
        result = self.db.query(ContributiontextModel).filter(ContributiontextModel.id == id).first()
        return result
    
    def delete_contributiontext(self,id:int):
        contributiontext = self.get_contributiontext_by_id(id)
        if not contributiontext:
            return None
        self.db.delete(contributiontext)
        self.db.commit()
        return contributiontext

    
    def update_contributiontext(self,id:int, contributiontext_schema:ContributiontextSchema):
        contributiontext= self.db.query(ContributiontextModel).get(id)
        if contributiontext:
            contributiontext.contribution_id = contributiontext_schema.contribution_id
            contributiontext.contribution_text = contributiontext_schema.contribution_text
            self.db.commit()
            return True
        return False
    
