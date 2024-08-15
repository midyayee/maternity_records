import enum
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import mapped_column, Mapped
#from app import app
from models import Base, BaseModel

class Role(enum.Enum):
    ADMIN = 'admin'
    CLIENT = 'client'
    CLINICAL = 'clinical'


class User(Base, BaseModel):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    role:Mapped[Role]
    created_at:Mapped[str] = mapped_column(DateTime, default=func.now())