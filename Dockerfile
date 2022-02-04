FROM python:3-alpine AS build
# upgrade pip
RUN pip install --upgrade pip
# add build pkgs
#RUN apk add --update gcc libc-dev jpeg-dev zlib-dev \
#&& rm  -rf /tmp/* /var/cache/apk/*
# install python modules
ADD dockerfiles/requirements.txt /
RUN pip install -r /requirements.txt

FROM python:3-alpine AS run
# add openssh and clean
RUN apk add --update bash openssh jpeg \
&& rm  -rf /tmp/* /var/cache/apk/*
# get compiled modules from pervious stage
COPY --from=build /usr/local/lib/python3.10 /usr/local/lib/python3.10
# add entrypoint script
ADD dockerfiles/docker-entrypoint.sh /usr/local/bin
# add sshd files
ADD dockerfiles/ssh* /etc/ssh/
# add ted user
RUN echo -e "m00nch1ld\nm00nch1ld" | adduser ted
# add the python files for the game
ADD dockerfiles/play.sh /usr/local/bin/play
ADD ./*.py /home/ted/
ADD ./json/ /home/ted/json/
# set permissions
RUN mkdir /home/ted/save-states
RUN chown -R root:root /home/ted
RUN chmod -R 755 /home/ted
RUN chmod -R 777 /home/ted/save-states
# finish up container
EXPOSE 22
ENTRYPOINT ["docker-entrypoint.sh"]
WORKDIR /home/ted/
CMD ["/usr/sbin/sshd","-D"]
