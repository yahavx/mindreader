#!/bin/bash

sudo docker network create local_net  # create network named local

MongoDB: sudo docker run -d -p 27017:27017 --name mongo --network my-net -v ~/data:/data/db mongo



sudo docker run -d -p 5000:5000 --name api --network local_net -v ~/mindreader(local folder):/home/user/mindreader(shared folder)
 -e DB_URL=mongodb://mongo:27017 thoughts-api(image name)

API: sudo docker run -d -p 5000:5000  --name api --network my-net -v ~/thoughts:/home/user/thoughts -e DB_URL=mongodb://mongo:27017 thoughts-api

Parsers: sudo docker run -d --name parsers --network my-net -v ~/thoughts:/home/user/thoughts -e MQ_URL=rabbitmq://rabit:5672 thoughts-parsers

RabitMQ: sudo docker run -d -p 5672:5672 --name rabit --network my-net rabbitmq

Saver: sudo docker run --name saver --network my-net -v ~/thoughts:/home/user/thoughts
-e DB_URL=mongodb://mongo:27017  -e MQ_URL=rabbitmq://rabit:5672 thoughts-saver

Server: sudo docker run -p 8000:8000  --name server --network my-net -v ~/thoughts:/home/user/thoughts -e MQ_URL=rabbitmq://rabit:5672 thoughts-server



sudo docker ps - view docker list
docker stop <id> - stop a docker

sudo docker start api - if already started and stopped before, can use this

sudo docker build -f Dockerfile-parsers -t thoughts-parsers(docker name after) .
sudo docker rm <dockername> - remove a docker