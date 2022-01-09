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
    *)
        echo "Invalid input, expecting local or remote"
        exit 1
    ;;
esac
