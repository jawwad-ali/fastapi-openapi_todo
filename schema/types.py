from pydantic import BaseModel

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey, Column, Integer, String

from typing import Union

class UserModel(BaseModel):
    username: str
    email: str
    password: str

class SystemUser(BaseModel):
    id: int
    username: str
    email: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    
class TokenPayload(BaseModel):
    # sub: int = None
    sub: Union[int, str] = None
    exp: int = None

# SQL ALCHEMY MODELS
    
Base = declarative_base()

class Todo(Base):
    __tablename__ = "project_todos"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    # Add a foreign key to link the Todo to a User
    user_email = Column(String, ForeignKey('project_users.email'))
    
    # Define the relationship
    user = relationship('User', back_populates='todos')


class User(Base):
    __tablename__ = "project_users"

    id = Column(Integer, primary_key=True)
    username = Column(String) 
    email = Column(String, unique=True)
    password = Column(String)

    # Establish the reverse relationship from User to Todo
    todos = relationship('Todo', back_populates='user')