FROM python:3.11

WORKDIR /app

ADD ./requirements.txt /app/requirements.txt

RUN pip install -U pip && pip install -r requirements.txt

ADD . /app

VOLUME [ "." ]

CMD python app.py