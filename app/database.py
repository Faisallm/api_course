from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# we are only changing this part.
# every thing else is boilerplate.
# it's good not to hard code this into your code.
# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:Faisal@localhost:5432/api_course"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# when we want to talk to the database, we have to make use...
# of a session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency (for communicating with the db)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()