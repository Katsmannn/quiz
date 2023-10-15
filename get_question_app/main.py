import asyncio

import aiohttp
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine


url = 'https://jservice.io/api/random'
params = {'count': 1}

MAX_FAILS = 50  # max numbers of fail query

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/question_count/')
def get_guestion_count(db: Session = Depends(get_db)):
    ''' Get number all questions in db. '''

    return crud.q_count(db=db)

@app.post('/get_questions/')
async def get_questions(query: schemas.MyQuery, db: Session = Depends(get_db)):
    questions = []
    fails = 0

    async with aiohttp.ClientSession() as session:

        while len(questions) < query.questions_num:
            async with session.get(url, params=params) as resp:
                response = await resp.json()
                if crud.is_question_exists(db=db, id=response[0]['id']):
                    fails += 1
                    if fails >= MAX_FAILS:
                        raise HTTPException(
                            status_code=400, detail="Not found"
                        )
                    continue
                else:
                    question=schemas.Question(
                        id=response[0]['id'],
                        created_at=response[0]['created_at'],
                        question=response[0]['question'],
                        answer=response[0]['answer']
                    )
                    questions.append(question)
        crud.create_questions(db=db, questions=questions)

    return questions[-1]
