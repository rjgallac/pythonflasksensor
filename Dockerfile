FROM python:3.14.0a6-alpine3.21
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./src/hello.py /app/hello.py
CMD ["python","-m","flask","--app", "hello", "run"]