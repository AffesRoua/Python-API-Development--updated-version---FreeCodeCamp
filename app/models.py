from .database import Base
from sqlalchemy import Integer, String,Boolean,Integer,Column,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import Relationship

class Post(Base):
    __tablename__="posts"
    id = Column(Integer, primary_key=True,nullable=False,autoincrement=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner=Relationship("Users") #here users is the class name not table name

class Users(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True,nullable=False,autoincrement=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    phone_number=Column(String)

class Vote(Base):
    __tablename__="votes"
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)

