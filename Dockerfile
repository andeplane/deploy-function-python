FROM python:3-alpine

COPY . /

RUN pip install cognite-sdk-experimental

CMD python src/index.py
