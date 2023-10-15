FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app

RUN python3 -m pip install --upgrade pip && pip3 install -r /app/requirements.txt --no-cache-dir

COPY get_question_app/ /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]