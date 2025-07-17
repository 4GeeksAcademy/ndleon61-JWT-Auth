from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256),nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    def __init__(self, email, password, is_active = True):
        self.email = email
        self.password = generate_password_hash(password)
        self.is_active = is_active
    
    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }