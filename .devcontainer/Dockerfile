FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN sudo apt update && sudo apt install -y iputils-ping
ADD https://downloads.mongodb.com/compass/mongodb-mongosh_2.5.2_amd64.deb mongo.deb
RUN sudo apt install ./mongo.deb -y