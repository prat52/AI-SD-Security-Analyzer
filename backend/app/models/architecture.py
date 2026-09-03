from sqlalchemy import JSON, Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base
from sqlalchemy.dialects.postgresql import JSONB




# class Architecture(Base):
#     __tablename__ = "architectures"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)

#     user_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="architectures")

class Architecture(Base):
    __tablename__ = "architectures"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    # response = Column(Text, nullable=True)
    response = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="architectures")