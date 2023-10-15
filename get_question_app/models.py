from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    question = Column(Text)
    answer = Column(String)
