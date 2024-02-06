pipeline {
    agent {node 'agent1'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
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
                    sh "docker login -u $DOCKERHUB_CREDENTIALS_USR -p $DDOCKERHUB_CREDENTIALS_PSW"

                    sh "docker push aviadbarel/weather_app"
                }
            }
        }
//         stage('Deploy') {
//             when {
//                 expression { currentBuild.currentResult == 'SUCCESS' }
//             }
//             steps {
//
//             }
//         }
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
            sh 'docker rm -f python_project'
            }
    }
}