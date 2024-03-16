pipeline {
    agent {node 'agent1'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        SSH_CREDENTIALS_ID = 'Sshdeploy'
        SSH_CREDENTIALS_KEY = credentials("${SSH_CREDENTIALS_ID}")
        TARGET_HOST = '172.31.40.29'
    }

    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                script {
                    sh 'docker build . -t weather_app'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run tests
                    sh 'docker run -d -p 80:8000 --name test aviadbarel/weather_app '
                    sh 'python3 tests/test.py'
                    sh 'docker rm -f test'
                }
            }
        }
        stage ('Push') {
            steps{
                script {
                    sh "docker tag weather_app aviadbarel/weather_app:${BUILD_NUMBER}"
                    sh 'docker tag weather_app aviadbarel/weather_app:latest'
                    sh "docker login -u ${DOCKERHUB_CREDENTIALS_USR} -p ${DOCKERHUB_CREDENTIALS_PSW}"
                    sh "docker push aviadbarel/weather_app:${BUILD_NUMBER} aviadbarel/weather_app:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                script{
                    sh "ssh-keyscan -v -H ${TARGET_HOST} >> ~/.ssh/known_hosts"
//                     sh "scp -i ${SSH_CREDENTIALS_KEY} compose.yml ec2-user@${TARGET_HOST}:/home/ec2-user"
//                     sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker-compose down"
                    sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker pull aviadbarel/weather_app"
                    sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker rm -f weather_app && docker run -d -p 80:8000 --name weather_app aviadbarel/weather_app"
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
            sh 'docker image rm -f aviadbarel/weather_app'
            sh 'docker logout'
            }
    }
}