FROM tiangolo/uwsgi-nginx-flask:python2.7



MAINTAINER Luana Martelli & Mika Pagani




COPY ./app ./app

COPY ./requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt




RUN pylama ./app/app.py ./app/mosaic.py ./app/load-database.py ./app/mail.py
CMD [ "python", "app/app.py"]
