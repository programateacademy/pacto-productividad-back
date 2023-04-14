from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import SessionLocal

from models.comments import Comments as CommentModel
from schemas.comment import Comment as CommentSchema

class CommentService():
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

    # auth
    def get_comments(self):
        result = self.db.query(CommentModel).all()
        return result
    
    def create_comment(self, comment:CommentModel):
        # current_user = ServiceToken.get_current_active_userid()
        comment_model = CommentModel(
        id_post= comment.id_post,
        status = comment.status,
        description = comment.description,
        likes= comment.likes,
        created_at = comment.created_at,
        updated_at = comment.updated_at,
        )
        self.db.add(comment_model)
        self.db.commit()
        return
    
    def get_comment_by_id(self,id:int):
        result = self.db.query(CommentModel).filter(CommentModel.id == id).first()
        return result
    
    def delete_comment(self,id:int):
        comment = self.get_comment_by_id(id)
        if not comment:
            return None
        self.db.delete(comment)
        self.db.commit()
        return comment

    def get_comment_by_status(self, status: str):
        comment_model = self.db.query(CommentModel).filter(CommentModel.status == status).all()
        if comment_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Status does not exist"
            )
        return comment_model
    
    def update_comment(self,id:int, comment_schema:CommentSchema):
        comment= self.db.query(CommentModel).get(id)
        if comment:
            comment.status = comment_schema.status
            comment.description = comment_schema.description
            comment.likes=comment_schema.likes
            comment.created_at = comment_schema.created_at
            comment.updated_at = comment_schema.updated_at

            self.db.commit()
            return True
        return False
    
