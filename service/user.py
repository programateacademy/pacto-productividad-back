from fastapi import FastAPI, HTTPException, Depends, status
from models.user import Users as UserModel
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from schemas.user import User as UserSchema
from database import SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import bcrypt
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
class UserService():
    # Create an instance of the CryptContext class for password hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # Create an instance of the OAuth2PasswordBearer class for authentication
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def get_db():
        # Helper method to get a database session. Yields:SQLAlchemy session
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()


    # Returns all users from the database.
    def get_users(self):
        result = self.db.query(UserModel).all()
        return result
        
    # Creates a new user in the database.
    def create_user(self, user:UserModel):
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        user_model = UserModel(
        id_type_actor = user.id_type_actor,
        id_city = user.id_city,
        id_contribution= user.id_contribution,
        name_user = user.name_user,
        lastname = user.lastname,
        email = user.email,
        username = user.username,
        password = hashed_password,
        cohabitation_agreement = user.cohabitation_agreement,
        type_user = user.type_user,
        name_enti = user.name_enti,
        contribution_text = user.contribution_text,
        status = user.status,
        description = user.description,
        knowledge_interests = user.knowledge_interests,
        created_at = user.created_at,
        updated_at = user.updated_at,
        forgot_password = user.forgot_password,
        image_profile = user.image_profile,
        phone_number = user.phone_number
        )
        self.db.add(user_model)
        self.db.commit()
        return
    
    # Returns a user by their ID.
    def get_user_by_id(self,id:int):
        result = self.db.query(UserModel).filter(UserModel.id == id).first()
        return result
    
    # Deletes a user by their ID.
    def delete_user(self,id:int):
        user = self.get_user_by_id(id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return user

    # Returns a user by their username.
    def get_user_by_username(self, username: str):
        user_model = self.db.query(UserModel).filter(UserModel.username == username).first()
        if user_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Username {username} does not exist"
            )
        return user_model
    
    # Updatin user by their ID
    def update_user(self,id:int, user_schema:UserSchema):
        user = self.db.query(UserModel).get(id)
        if user:
            user.id_type_actor=user_schema.id_type_actor
            user.id_city = user_schema.id_city
            user.id_contribution = user_schema.id_contribution
            user.name_user=user_schema.name_user
            user.lastname = user_schema.lastname
            user.email = user_schema.email
            user.username = user_schema.username
            user.password = user_schema.password
            user.cohabitation_agreement = user_schema.cohabitation_agreement
            user.status = user_schema.status
            user.type_user = user_schema.type_user
            user.name_enti = user_schema.name_enti
            user.contribution_text = user_schema.contribution_text,
            user.description = user_schema.description
            user.knowledge_interests = user_schema.knowledge_interests
            user.created_at = user_schema.created_at
            user.updated_at = user_schema.updated_at
            user.forgot_password = user_schema.forgot_password
            user.image_profile = user_schema.image_profile
            user.phone_number = user_schema.phone_number
            self.db.commit()
            return True
        return False
    

    # RESET PW SERVICE
    def generar_contraseña_aleatoria():
        longitud = 12
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = "".join(random.choice(caracteres) for i in range(longitud))
        return contraseña

    def enviar_correo(email_json, contraseña):
        email = email_json['email']
        remitente = 'zulmadirectv@gmail.com'
        destinatario = email
        asunto = 'Nueva contraseña para tu cuenta'
        cuerpo = f'Hola,\n\nTu nueva contraseña es: {contraseña}\n\nPor favor, cambia tu contraseña en cuanto inicies sesión.\n\nSaludos,\nEl equipo de PACTO'

        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, 'mqjeppxuvadguzjw')
        texto = mensaje.as_string()
        servidor.sendmail(remitente, destinatario, texto)
        servidor.quit()

    # SAVE IMG PROFILE
