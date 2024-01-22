import os

from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine

from sqlalchemy.orm import Session, sessionmaker, declarative_base

# for key, value in os.environ.items():
#     print(f'{key}: {value}') 

######## DB
dbConnectionStr = os.environ["DB_KEY"] 
conn_str = dbConnectionStr

engine: Engine = create_engine(conn_str)

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()

Base.metadata.create_all(engine)

def get_db():
    db = Session() 
    try:
        yield db
    finally:
        db.close()

######## DB CLOSE