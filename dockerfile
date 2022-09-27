FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN apk add --update --no-cache graphviz ttf-dejavu \
  && addgroup -g 1000 dot \
  && adduser -u 1000 -G dot -s /bin/sh -D dot && pip install -r requirements.txt

# CMD python app.py
ENTRYPOINT python app.py
