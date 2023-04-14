from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.contributions import Contribution as ContributionModel
from schemas.contribution import Contribution as ContributionSchema

class ContributionService():
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

    def get_contribution(self):
        result = self.db.query(ContributionModel).all()
        return result
    
    def create_contribution(self, contribution:ContributionModel):
        # current_user = ServiceToken.get_current_active_userid()
        contribution_model = ContributionModel(
        name = contribution.name
        )
        self.db.add(contribution_model)
        self.db.commit()
        return
    
    def get_contribution_by_id(self,id:int):
        result = self.db.query(ContributionModel).filter(ContributionModel.id == id).first()
        return result
    
    def delete_contribution(self,id:int):
        contribution = self.get_contribution_by_id(id)
        if not contribution:
            return None
        self.db.delete(contribution)
        self.db.commit()
        return contribution

    
    def update_contribution(self,id:int, contribution_schema:ContributionSchema):
        Contribution= self.db.query(ContributionModel).get(id)
        if Contribution:
            Contribution.name = contribution_schema.name
            self.db.commit()
            return True
        return False
    