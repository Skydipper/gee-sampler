FROM python:3.7-alpine
MAINTAINER Enrique Cornejo enrique.cornejo@vizzuality.com

ENV NAME gee_sampler
ENV USER gee_sampler

RUN apk update && apk upgrade && \
   apk add --no-cache --update bash git openssl-dev build-base alpine-sdk \
   libffi-dev gcc python3-dev musl-dev

RUN addgroup $USER && adduser -s /bin/bash -D -G $USER $USER

RUN easy_install pip && pip install --upgrade pip
RUN pip install virtualenv gunicorn gevent

RUN mkdir -p /opt/$NAME
RUN cd /opt/$NAME && virtualenv venv && source venv/bin/activate
COPY requirements.txt /opt/$NAME/requirements.txt
RUN cd /opt/$NAME && pip install -r requirements.txt

COPY entrypoint.sh /opt/$NAME/entrypoint.sh
COPY main.py /opt/$NAME/main.py
COPY test.py /opt/$NAME/test.py
COPY gunicorn.py /opt/$NAME/gunicorn.py

# Copy the application folder inside the container
WORKDIR /opt/$NAME

COPY ./$NAME /opt/$NAME/$NAME
COPY ./microservice /opt/$NAME/microservice
RUN chown $USER:$USER /opt/$NAME

# Tell Docker we are going to use this ports
EXPOSE 5650
USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]
