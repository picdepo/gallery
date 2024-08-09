FROM alpine:3.18.2

WORKDIR /flask

RUN apk add python3 py3-pip

RUN pip3 install --upgrade pip

COPY ./ /flask/

RUN pip install -r requirements.txt

CMD [ "python3", "/flask/app.py" ]
