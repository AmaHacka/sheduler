FROM python:3.8
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./sheduler /code/
EXPOSE 80
ENTRYPOINT python manage.py runserver 0.0.0.0:80 --insecure
