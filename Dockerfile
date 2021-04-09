FROM python:3.7-slim-buster

WORKDIR /app

RUN apt update && apt install -y build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONPATH=/app

ENV DATA="data/db.csv"
ENV TREE="data/tree.ann"

EXPOSE 80

CMD python3 app.py \
    --data $DATA \
    --tree $TREE
