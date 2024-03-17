FROM python:3.10.13-alpine
WORKDIR /project
COPY ./app .
RUN pip install -r requirements.txt
CMD gunicorn -w 5 -b 0.0.0.0:8000 main:app
EXPOSE 8000