pipeline {
    agent {node 'agent1'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        SSH_CREDENTIALS = credentials('Sshdeploy')
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
                    sh 'docker build . -t aviadbarel/weather_app'
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
                sh "echo ${SSH_CREDENTIALS_KEY}"
                sh "ssh -i ${SSH_CREDENTIALS} ec2-user@172.31.40.29 docker image rm -f aviadbarel/weather_app"
                sh "ssh -i ${SSH_CREDENTIALS} ec2-user@172.31.40.29 docker-compose up -d --build"
                }
            }
        }
    }
    post {
//         success{
//             slackSend(channel: '', color: 'good', message: "Tests passed! build: ${BUILD_NUMBER} commit: ${GIT_COMMIT}")
//         }
//         failed{
//             slackSend(channel: '', color: 'danger', message: "Tests failed! ${BUILD_NUMBER} commit: ${GIT_COMMIT}")
//         }
        always {
            cleanWs()
            sh 'docker rm -f weather_app'
            }
    }
}