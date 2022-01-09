#!/usr/bin/env bash

case $1 in
    *)
        docker-compose up --build
    ;;
    docker)
        docker build --tag ted-moonchild .
        docker run -it --rm --name ted-moonchild-and-the-roadies-in-space ted-moonchild
    ;;
esac
