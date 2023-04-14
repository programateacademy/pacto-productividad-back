from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal


from models.post import Posts as PostModel
from schemas.post import Post as PostSchema
# from service.token import user_token as ServiceToken

class PostService():
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
    def get_posts(self):
        result = self.db.query(PostModel).all()
        return result
    
    def create_post(self, post:PostModel):
        # current_user = ServiceToken.get_current_active_userid()
        post_model = PostModel(
        id_user= post.id_user,
        status = post.status,
        description = post.description,
        created_at = post.created_at,
        updated_at = post.updated_at,
        image_post = post.image_post,
        video_post = post.video_post,
        document_post = post.document_post,
        )
        self.db.add(post_model)
        self.db.commit()
        return
    
    def get_post_by_id(self,id:int):
        result = self.db.query(PostModel).filter(PostModel.id == id).first()
        return result
    
    def delete_post(self,id:int):
        post = self.get_post_by_id(id)
        if not post:
            return None
        self.db.delete(post)
        self.db.commit()
        return post

    def get_post_by_status(self, status: str):
        post_model = self.db.query(PostModel).filter(PostModel.status == status).all()
        if post_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Status does not exist"
            )
        return post_model
    
    def update_post(self,id:int, post_schema:PostSchema):
        post = self.db.query(PostModel).get(id)
        if post:
            post.status = post_schema.status
            post.description = post_schema.description
            post.created_at = post_schema.created_at
            post.updated_at = post_schema.updated_at
            post.image_post = post_schema.image_post
            post.video_post = post_schema.video_post
            post.document_post = post_schema.document_post
            self.db.commit()
            return True
        return False
    
