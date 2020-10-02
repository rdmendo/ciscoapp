FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
COPY . /app
WORKDIR /app
ENV STATIC_PATH /app/ciscoapp/static
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del build-dependencies

  
# ENTRYPOINT [ "python" ] 
# CMD [ "run.py" ] 