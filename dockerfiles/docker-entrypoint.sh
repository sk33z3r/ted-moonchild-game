#!/bin/sh

if [ ! -f "/etc/ssh/ssh_host_rsa_key" ]; then
	echo "Host RSA Key missing."
	exit 1
fi
if [ ! -f "/etc/ssh/ssh_host_dsa_key" ]; then
	echo "Host DSA Key missing."
	exit 1
fi

#prepare run dir
if [ ! -d "/var/run/sshd" ]; then
  mkdir -p /var/run/sshd
fi

exec "$@"
