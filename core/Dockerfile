FROM python:3.8-slim

RUN mkdir -p /home/app && pip install --upgrade pip setuptools wheel && pip install mysql-connector-python && pip install scipy

COPY . /home/app

CMD ["python", "home/app/app.py"]