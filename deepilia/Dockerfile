FROM python:3.8-slim

# allows for live python output in docker logs 
ENV PYTHONUNBUFFERED=1

# creating workdir in the container
RUN mkdir /code
WORKDIR /code

# installing required python modules
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

ADD . /code/