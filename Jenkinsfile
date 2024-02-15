pipeline {
    agent {node 'agent1'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        SSH_CREDENTIALS_ID = 'Sshdeploy'
        SSH_CREDENTIALS_KEY = credentials("${SSH_CREDENTIALS_ID}")
        TARGET_HOST = '172.31.40.29'
        version=readfile('./v.txt').trim()
    }

    stages {
        stage('Build') {
            steps {
                script {
                    sh 'docker build . -t aviadbarel/weather_app'
                }
            }
        }
        stage('Tests') {
            steps {
                script {
                    // Run tests
                    sh 'docker compose up -d'
                    sh 'python3 tests/test.py'
                    sh 'python3 tests/test_selenium.py'
                }
            }
        }
        
        stage ('Delivery') {
            when{
                branch 'pre-production'
            }
            steps{
                script {
                    sh "docker tag aviadbarel/weather_app aviadbarel/weather_app:latest"
                    sh "docker tag aviadbarel/weather_app aviadbarel/weather_app:${version}-${BUILD_NUMBER}"
                    sh "docker login -u ${DOCKERHUB_CREDENTIALS_USR} -p ${DOCKERHUB_CREDENTIALS_PSW}"
                    sh "docker push aviadbarel/weather_app:latest"
                    sh "docker push aviadbarel/weather_app:${version}-${BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy') {
            when{
                branch 'production'
            }
            steps {
                script{
                    sh "ssh-keyscan -v -H ${TARGET_HOST} >> ~/.ssh/known_hosts"
                    // sh "scp -i ${SSH_CREDENTIALS_KEY} compose.yml ec2-user@${TARGET_HOST}:/home/ec2-user"
                    sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker-compose stop && docker-compose rm -f"
                    sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker-compose pull && docker-compose up -d"
                }
            }
        }
    }
    post {
        success{
            slackSend(channel: 'succeeded-build', color: 'good', message: "Tests passed! build: ${BUILD_NUMBER} commit: ${GIT_COMMIT}")
        }
        failure{
            slackSend(channel: 'devops-alert', color: 'danger', message: "Tests failed! ${BUILD_NUMBER} commit: ${GIT_COMMIT}")
        } 

        always {
            cleanWs()
            sh 'docker compose down'
            sh 'docker image rm -f aviadbarel/weather_app'
            sh 'docker logout'
            }
    }
}