FROM python:3.8-slim
 
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./models /code/models

ENV MODEL_PATH=/code/models/v0.0.2.pkl

CMD ["hypercorn", "app.main:app", "--bind", "0.0.0.0:8080", "--workers","2", "--graceful-timeout", "20"]
