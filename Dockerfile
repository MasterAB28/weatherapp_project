FROM ubuntu:latest
RUN apt update && apt install -y python3 python3-pip
WORKDIR project
COPY app .
RUN pip install -r requirements.txt
CMD gunicorn -w 5 main:app -b 0.0.0.0:8000
EXPOSE 8000