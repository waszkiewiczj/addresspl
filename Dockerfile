FROM python:3.8-slim-buster

WORKDIR /app

RUN apt update && apt install -y build-essential

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONPATH=/app

ARG SIMC_CSV="data/SIMC_Urzedowy_2021-04-06.csv"
ARG ULIC_CSV="data/ULIC_Adresowy_2021-04-06.csv"

ENV DATA="data/db.csv"
ENV TREE="data/tree.ann"

RUN python clean_data.py \
    --simc-csv $SIMC_CSV \
    --ulic-csv $ULIC_CSV \
    --out-path $DATA

RUN python build_annoy.py \
    --csv-path $DATA \
    --col-name STRING \
    --out $TREE

EXPOSE 80

CMD python app.py \
    --data $DATA \
    --tree $TREE
