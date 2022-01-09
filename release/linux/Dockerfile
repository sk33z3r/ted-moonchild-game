FROM python:3-alpine
# upgrade pip
RUN pip install --upgrade pip
# install python modules
ADD dockerfiles/requirements.txt /
RUN pip install -r /requirements.txt
# add the python files for the game
ADD main.py /tmatris/
ADD asciiGFX.py /tmatris/
# finish up container
WORKDIR /tmatris
CMD ["python","main.py"]
