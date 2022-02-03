FROM python:3-alpine
# upgrade pip
RUN pip install --upgrade pip
# add build pkgs
#RUN apk add --update gcc libc-dev jpeg-dev zlib-dev \
#&& rm  -rf /tmp/* /var/cache/apk/*
# install python modules
ADD requirements.txt /
RUN pip install -r /requirements.txt
# add the python files for the game
ADD ./*.py /tmatris/
ADD ./json/ /tmatris/json/
# finish up container
WORKDIR /tmatris
CMD ["python","main.py"]
