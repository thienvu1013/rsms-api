FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./src /app/src

COPY ./requirements.txt /app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 

RUN pip3 install -r requirements.txt

EXPOSE 80
EXPOSE 443

CMD ["uvicorn", "src.main:api", "--host", "0.0.0.0", "--port", "${PORT:-5000}", "--forwarded-allow-ips", "*"]


