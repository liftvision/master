FROM python:3.9-slim


WORKDIR /app

RUN apt update && apt install -y gcc

COPY requirements.txt /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt


COPY app /app

CMD ["./entrypoint.sh"]
