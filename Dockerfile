FROM python:3-alpine

COPY . /

# RUN npm install cognite-sdk
RUN npm install cognite-sdk-experimental

CMD python src/index.py
