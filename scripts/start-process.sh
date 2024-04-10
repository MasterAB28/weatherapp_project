#!/bin/bash

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/v7l9w0u1

docker pull public.ecr.aws/v7l9w0u1/nginx:latest
docker pull public.ecr.aws/v7l9w0u1/weather_app:latest

docker image tag public.ecr.aws/v7l9w0u1/nginx:latest aviadbarel/nginx:latest
docker image tag public.ecr.aws/v7l9w0u1/weather_app:latest aviadbarel/weather_app:latest

#deploy=$(aws deploy list-deployments --application-name weather_app --deployment-group-name weather_app | jq -r '.deployments[0]')
#
#docker-compose --project-directory "/opt/codedeploy-agent/deployment-root/721aa903-fe9d-42ea-8d40-00fa8d155ddd/$deploy/deployment-archive/" up -d

cd /home/ec2-user && docker-compose up -d