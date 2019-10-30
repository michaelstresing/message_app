from datetime import datetime
from . import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.sql import func
from flask_login import UserMixin
from uuid import uuid4
from application import login

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


@login.user_loader
def load_user(username):
    return User.query.get(username)


chat_lookup = Table('chat_users', db.Model.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('chat_id', Integer, ForeignKey('chats.chat_id'))
)


class User(UserMixin, db.Model):
    """Data model for Users"""

    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=uuid4)
    username  = Column(String(64), index=True, unique=True)
    first_name = Column(String(64), index=True)
    last_name = Column(String(64), index=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))
    salt = Column(String(64), default=None)
    datecreated = Column(DateTime(timezone=True),
                             server_default=func.now())
    dateupdated = Column(DateTime, default=None)
    profpic = Column(String(128), default=None)
    chats = relationship("Chat",
                        secondary=chat_lookup,
                        back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def from_user(dict):

        return User(
            username=dict['username'],
            first_name=dict['first_name'],
            last_name =dict['last_name'],
            email=dict['email'],
            password_hash=dict['password_hash'], 
            )

    def to_user(self):
       """Return object data in easily serializable format"""
       return {
            'id'  : self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email':self.email,
            'password_hash':self.password_hash,
            'salf':self.salt,
            'datecreated':self.datecreated,
            'dateupdated':self.dateupdated
       }


class Chat(db.Model):
    """ Data Model for Conversations"""

    __tablename__ = 'chats'

    chat_id = Column(Integer, primary_key=True)
    chatname = Column(String(64), index=True)
    datecreated = Column(DateTime(timezone=True),
                             server_default=func.now())
    messagessent = Column(Integer, default=None)
    users = relationship("User",
                        secondary=chat_lookup,
                        back_populates='chats')

    @staticmethod
    def from_chat(dict):

        return Chat(
            # chat_id =dict['chat_id'],
            chatname =dict['chatname']
            # datecreated =dict['datecreated'],
            # messagessent =dict['messagessent']
        )
    
    def to_chat(self):

        return {
            'chat_id' : self.chat_id,
            'chatname': self.chatname,
            'datecreated': self.datecreated,
            'messagessent': self.messagessent
        }


class Message(db.Model):

    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey('chats.chat_id'))
    sender_id = Column(String, ForeignKey('users.id'))
    content = Column(String)
    timesent = Column(DateTime(timezone=True),
                             server_default=func.now())

    @staticmethod
    def from_messages(dict, chat_id, user_id):

        return Message(

            sender_id = user_id,
            content =dict['content'],
        )
    
    def to_messages(self):

        return {
        'message_id': self.message_id,
        'chat_id': self.chat_id,
        'sender_id': self.sender_id,
        'content': self.content,
        'timesent': self.timesent
        }
