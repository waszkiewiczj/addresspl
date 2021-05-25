FROM python:3.7-slim-buster as base
WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY data data
COPY src src

FROM base as test
COPY test test
RUN pytest test

FROM base as serving
RUN useradd -M server
USER server
EXPOSE 80
CMD python src
