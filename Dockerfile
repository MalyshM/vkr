# Backend
FROM python:3.10 as backend

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app
RUN pip install cryptography
RUN pip install --no-cache-dir -r requirements.txt

# Frontend
FROM node:14 as frontend

WORKDIR /react_app
COPY react_app/for_vlad/package*.json ./
RUN npm install
COPY frontend/for_vlad/ ./
RUN npm run build

# Combined image
FROM python:3.10

ENV PYTHONUNBUFFERED 1

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y nodejs \
    npm

EXPOSE 8000
WORKDIR /backend
COPY --from=backend /app /app
COPY --from=frontend /react_app/build /app/react_app

RUN pip install cryptography
RUN pip install --no-cache-dir -r requirements.txt