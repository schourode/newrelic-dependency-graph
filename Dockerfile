FROM python:3.6.4

WORKDIR /app

RUN apt-get update && \
    apt-get install -y graphviz && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

CMD [ "python", "newrelic.py" ]
