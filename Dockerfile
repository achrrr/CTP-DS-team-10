FROM python:3.11

RUN apt-get update && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY . /app/

RUN pip3 install -r requirements.txt

CMD ["flask", "--app", "client", "run", "--host", "0.0.0.0"]

