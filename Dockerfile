FROM python:3.9

ENV APP_HOME /index
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python index.py