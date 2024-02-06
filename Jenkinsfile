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
                    dir(./app){
                        sh 'docker build . -t aviadbarel/weather_app'
                    }
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run tests
                    sh 'docker run -p 8000:8000 -d --name weather_app aviadbarel/weather_app'

                    sh 'python3 test.py'
                }
            }
        }
        stage ('Push') {
            steps{
                script {
                    sh "docker login -u ${DOCKERHUB_CREDENTIALS_USR} -p ${DOCKERHUB_CREDENTIALS_PSW}"

                    sh "docker push aviadbarel/weather_app"
                }
            }
        }

        stage('Deploy') {
            steps {
                script{
                sh "ssh-keyscan -H ${TARGET_HOST} >> ~/.ssh/known_hosts"
                sh "echo ${SSH_CREDENTIALS_KEY}"
                sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker image rm -f aviadbarel/weather_app"
                sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker-compose up -d --build"
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
            sh 'docker rm -f weather_app'
            }
    }
}