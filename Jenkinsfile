pipeline {
    agent {node 'agent1'}

    stages {
        stage('Build') {
            steps {
                script {
                    git branch: 'master', url: 'https://gitlab.aviadapps.com/root/weather_app.git'
                    docker.Build('python_project')
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
            // Cleanup: Remove the Docker image after the tests
            cleanWs()
            sh 'docker logout'
        }
    }
}