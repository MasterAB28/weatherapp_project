#!/bin/bash


docker-compose down

docker rmi -f public.ecr.aws/v7l9w0u1/nginx:latest public.ecr.aws/v7l9w0u1/weather_app:latest

rm -f /home/ec2-user/compose.yml
