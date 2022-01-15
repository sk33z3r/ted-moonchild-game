#!/usr/bin/env bash

case $2 in
    debug|-d)
        command="play --debug"
    ;;
    *)
        command="play"
    ;;
esac

case $1 in
    local)
        ./server-run.sh && sleep 2
        ssh -p 7175 -o "LogLevel ERROR" -o "StrictHostKeyChecking no" -o "UserKnownHostsFile=/dev/null" -t ted@localhost "$command"
        docker-compose down
    ;;
    remote)
        ssh -p 7175 -o "LogLevel ERROR" -o "StrictHostKeyChecking no" -o "UserKnownHostsFile=/dev/null" -t ted@moonchild.space "$command"
    ;;
    env)
        docker-compose up -d mongo
        docker build -t tmatris-python .
        docker run -it --rm --name python -p 7175:22 --net tmatris --ip 172.200.0.120 -v $PWD:/home/ted tmatris-python bash
        docker-compose down
    ;;
    *)
        echo "Invalid input, expecting local or remote"
        exit 1
    ;;
esac
