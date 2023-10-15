from datetime import datetime

from pydantic import BaseModel


class MyQuery(BaseModel):
    questions_num: int


class Question(BaseModel):
    id: int
    created_at: datetime
    question: str
    answer: str

    class Config:
        orm_mode = True
