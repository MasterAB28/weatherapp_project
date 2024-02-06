pipeline {
    agent {node 'agent1'}

    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                script {
                    sh 'docker build . -t python_project'
                }
            }
        }
        stage('Test') {
            steps {
                script {
                    // Run tests
                    sh 'docker run -p 8000:8000 -d --name python_project python_project'
                    sh 'python3 test.py'

                    // Notify Slack based on test results
//                     if (testExitCode != 0) {
//                         slackSend(channel: '', color: 'danger', message: "Tests failed!")
//                         error 'Tests failed!'
//                     } else {
//                         slackSend(channel: '', color: 'good', message: "Tests passed!")
//                     }
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