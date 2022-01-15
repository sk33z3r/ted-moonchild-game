#!/usr/bin/env bash

if [ ! -f "dockerfiles/ssh_host_rsa_key" ]; then
	echo "Generating fresh rsa key"
	ssh-keygen -f dockerfiles/ssh_host_rsa_key -N '' -t rsa
fi
if [ ! -f "dockerfiles/ssh_host_dsa_key" ]; then
	echo "Generating fresh dsa key"
	ssh-keygen -f dockerfiles/ssh_host_dsa_key -N '' -t dsa
fi

docker-compose up -d --build --force-recreate
