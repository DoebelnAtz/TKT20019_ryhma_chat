from sqlalchemy import BigInteger, Text, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from . import db

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    username = db.Column(Text, nullable=False)
    password = db.Column(Text, nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class Group(Base):
    __tablename__ = 'groups'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(Text, nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class Message(Base):
    __tablename__ = 'messages'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    content = db.Column(Text, nullable=False)
    group_id = db.Column(BigInteger, ForeignKey('groups.id'), nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

class UserGroup(Base):
    __tablename__ = 'users_groups'
    user_id = db.Column(BigInteger, ForeignKey('users.id'), primary_key=True, nullable=False)
    group_id = db.Column(BigInteger, ForeignKey('groups.id'), primary_key=True, nullable=False)

class GroupInvite(Base):
    __tablename__ = 'group_invites'
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    group_id = db.Column(BigInteger, ForeignKey('groups.id'), nullable=False)
    sender_id = db.Column(BigInteger, ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(BigInteger, ForeignKey('users.id'), nullable=False)
    created_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = db.Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
