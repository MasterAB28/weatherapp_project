#!/bin/bash

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/v7l9w0u1

docker-compose down

docker image rm -f public.ecr.aws/v7l9w0u1/nginx:latest aviadbarel/nginx:latest public.ecr.aws/v7l9w0u1/weather_app:latest aviadbarel/weather_app:latest

docker pull public.ecr.aws/v7l9w0u1/nginx:latest
docker pull public.ecr.aws/v7l9w0u1/weather_app:latest

docker image tag public.ecr.aws/v7l9w0u1/nginx:latest aviadbarel/nginx:latest
docker image tag public.ecr.aws/v7l9w0u1/weather_app:latest aviadbarel/weather_app:latest
echo "hi"
pwd

docker-compose up -d