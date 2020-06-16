FROM ubuntu:16.04

MAINTAINER Van Nguyen "vanessanguyen382@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3" ]

CMD [ "app/setup.py", "app/api.py" ]