FROM python:3.11

MAINTAINER Dmitry

LABEL version="1"

WORKDIR '/booking'

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=8000"]
