from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String,  Boolean, text, ForeignKey
from sqlalchemy.orm import relationship

# each model represent a table in the database.

class Post(Base):
    __tablename__ = 'posts'

    # nullable indicates that it can't be left empty
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    # timestamp with timezone.
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text("now()"))
    
    # many-to-one relationship
    # a user can create multiple posts.
    # while each post is only associated with one user.
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # monkey-patching
    # when we retrieve a post...
    # it's going to return our user property asap
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    # no two accounts can have the same email.
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # time the user created his account.
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text("now()"))
    
    phone_number = Column(String)


class Vote(Base):
    """Composite keys store two foreign primary keys
    at the same time."""
    __tablename__ = "votes"

    # references the user's id
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    # references the post's id
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)