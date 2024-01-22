# from sqlalchemy.engine.base import Engine

# from sqlalchemy.orm import declarative_base, Session, sessionmaker, relationship

# from sqlalchemy import Column, Integer, String, create_engine, ForeignKey

# # from sqlalchemy.dialects.postgresql import UUID

# from pydantic import BaseModel

# # from uuid import UUID

# Base = declarative_base()

# # connection string of neon db
# # conn_str = f"postgresql://alijawwad001:N1LAc4gIlkZG@ep-tiny-sound-86380309.us-east-2.aws.neon.tech/neondb?sslmode=require"

# # engine: Engine = create_engine(conn_str)

# # Session = sessionmaker(bind=engine)
# # session = Session()

# # Database schema through sql alchemy
# # class Todo(Base):
# #     __tablename__ = "project_todos"

# #     id = Column(Integer , primary_key=True) 
# #     title = Column(String)
# #     description = Column(String)


# # class User(Base):
# #     __tablename__ = "project_users"

# #     # id = Column(UUID, primary_key=True)
# #     # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    
# #     id = Column(Integer , primary_key=True)
# #     username = Column(String)
# #     email = Column(String)
# #     password = Column(String) 


# class UserModel(BaseModel):
#     username: str
#     email: str
#     password: str

# class Todo(Base):
#     __tablename__ = "project_todos"

#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     description = Column(String)

#     # Add a foreign key to link the Todo to a User
#     user_id = Column(Integer, ForeignKey('project_users.email'))
    
#     # Define the relationship
#     user = relationship('User', back_populates='todos')

# class User(Base):
#     __tablename__ = "project_users"

#     id = Column(Integer, primary_key=True)
#     username = Column(String) 
#     email = Column(String)
#     password = Column(String)

#     # Establish the reverse relationship from User to Todo
#     todos = relationship('Todo', back_populates='user')

# Base.metadata.create_all(engine) 