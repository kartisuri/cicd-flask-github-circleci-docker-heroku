FROM python:3.6.2
LABEL maintainer kartisuri

COPY requirements.txt /app
ADD app /

WORKDIR /app

EXPOSE 5000

CMD python app.py
