from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import select, func

import models, schemas


def is_question_exists(db: Session, id: int):
    ''' Check question is in db. '''

    question = db.query(models.Question).filter(models.Question.id == id)
    return db.query(question.exists()).scalar()


def q_count(db: Session):
    ''' Get number all questions in db. '''

    return db.query(func.count(models.Question.id)).scalar()


def create_questions(db: Session, questions: List[schemas.Question]):
    ''' Add new question's list to db. '''

    new_questions = []
    for q in questions:
        new_question = models.Question(
            id=q.id,
            created_at=q.created_at,
            question=q.question,
            answer=q.answer
        )
        new_questions.append(new_question)
    db.add_all(new_questions)
    db.commit()
    return new_questions