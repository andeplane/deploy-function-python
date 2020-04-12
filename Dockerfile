# FROM andershaf/python3-cognite-sdk-experimental
FROM python:3

RUN apt-get install -y git
RUN pip install cognite-sdk-experimental

COPY . /
CMD python /src/index.py
