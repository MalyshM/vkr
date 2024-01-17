FROM node:node:20.10.0 as frontend

RUN apt-get update && apt-get upgrade -y
WORKDIR /
COPY . /frontend
# WORKDIR /
# COPY ./package*.json ./
RUN npm install
# COPY ./ ./



EXPOSE 8000