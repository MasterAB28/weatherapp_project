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
//         stage('Test') {
//             steps {
//                 script {
//                     // Run tests
//                     def testExitCode =
//
//                     // Notify Slack based on test results
//                     if (testExitCode != 0) {
//                         slackSend(channel: '', color: 'danger', message: "Tests failed!")
//                         error 'Tests failed!'
//                     } else {
//                         slackSend(channel: '', color: 'good', message: "Tests passed!")
//                     }
//                 }
//             }
//         }
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
        always {
            cleanWs()
            }
    }
}