FROM python:3.10

# requirements for app are installed
COPY ./requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip
RUN pip install -r /tmp/requirements.txt

# run backend app
WORKDIR /app
EXPOSE $DATA_MICROSERVICE_PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port $DATA_MICROSERVICE_PORT --reload