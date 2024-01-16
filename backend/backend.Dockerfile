# Backend
FROM python:3.10 as backend

ENV PYTHONUNBUFFERED 1

WORKDIR /
COPY . /backend
RUN pip install cryptography
RUN pip install --no-cache-dir -r /backend/requirements.txt

EXPOSE 8000