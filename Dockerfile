FROM python:3.8-slim-buster

WORKDIR /app

RUN apt update && apt install -y build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONPATH=/app

RUN python data.py && python build_annoy.py --csv-path data/db.csv --col-name STRING --out data/tree.ann

EXPOSE 80

CMD python app.py
