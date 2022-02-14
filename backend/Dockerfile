FROM python:3-alpine

RUN mkdir -p /home/app && pip install flask && pip install flask_limiter && pip install flask_accept && pip install mysql-connector-python && pip install flask-cors

COPY . /home/app

CMD ["python", "home/app/app.py"]
