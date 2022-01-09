FROM python:3-alpine
# upgrade pip
RUN pip install --upgrade pip
# add openssh and clean
RUN apk add --update openssh \
&& rm  -rf /tmp/* /var/cache/apk/*
# add entrypoint script
ADD dockerfiles/docker-entrypoint.sh /usr/local/bin
# add sshd files
ADD dockerfiles/ssh* /etc/ssh/
# install python modules
ADD dockerfiles/requirements.txt /
RUN pip install -r /requirements.txt
# add ted user
RUN echo -e "m00nch1ld\nm00nch1ld" | adduser ted
# add the python files for the game
ADD dockerfiles/play.sh /usr/local/bin/play
ADD main.py /home/ted/
ADD asciiGFX.py /home/ted/
# set permissions
RUN chown -R root:root /home/ted
RUN chmod -R 755 /home/ted
# finish up container
EXPOSE 22
ENTRYPOINT ["docker-entrypoint.sh"]
WORKDIR /tmatris
CMD ["/usr/sbin/sshd","-D"]
