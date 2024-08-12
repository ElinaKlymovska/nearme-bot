# database/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Credential(Base):
    username = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    requests = relationship("TikTokRequest", back_populates="credential")


class TikTokRequest(Base):
    chat_id = Column(Integer, index=True, nullable=True)
    credential_id = Column(Integer, ForeignKey('credential.id'), nullable=False)
    credential = relationship("Credential", back_populates="requests")
    hashtags = relationship("Hashtag", back_populates="request", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="request", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="request", cascade="all, delete-orphan")


class Hashtag(Base):
    request_id = Column(Integer, ForeignKey('tiktokrequest.id'), nullable=False)
    hashtag = Column(String, nullable=False)
    request = relationship("TikTokRequest", back_populates="hashtags")

    def __str__(self):
        return self.hashtag


class Comment(Base):
    request_id = Column(Integer, ForeignKey('tiktokrequest.id'), nullable=False)
    comment = Column(String, nullable=False)
    request = relationship("TikTokRequest", back_populates="comments")

    def __str__(self):
        return self.comment


class Message(Base):
    request_id = Column(Integer, ForeignKey('tiktokrequest.id'), nullable=False)
    message = Column(String, nullable=False)
    request = relationship("TikTokRequest", back_populates="messages")

    def __str__(self):
        return self.message
