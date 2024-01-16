FROM node:20 as frontend

RUN apt-get update && apt-get upgrade -y

# WORKDIR /
# COPY ./package*.json ./
# RUN npm install
# COPY ./ ./



EXPOSE 8000