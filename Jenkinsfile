pipeline {
    agent {node 'agent1'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        SSH_CREDENTIALS_ID = 'Sshdeploy'
        SSH_CREDENTIALS_KEY = credentials("${SSH_CREDENTIALS_ID}")
        TARGET_HOST = '172.31.40.29'
    }

    stages {

        stage('OWASP Dependency-Check Vulnerabilities') {
            steps {
                script{
                    sh "export JAVA_TOOL_OPTIONS = '-Xmx2g'"
                }
                dependencyCheck additionalArguments: ''' 
                            -o './'
                            -s './'
                            -f 'ALL' 
                            --prettyPrint''', odcInstallation: 'OWASP', nvdCredentialsId: 'NVD', stopBuild: true
                
                dependencyCheckPublisher pattern: 'dependency-check-report.xml'
            }
        }

        stage('Build') {
            steps {
                script {
                    sh 'docker build . -t weather_app'
                }
            }
        }
        stage('Tests') {
            steps {
                script {
                    // Run tests
                    sh 'docker run -d -p 80:8000 --name test weather_app '
                    sh 'python3 tests/test.py'
                    sh 'docker rm -f test'
                }
            }
        }
        stage ('Push') {
            when{
                branch 'main'
            }
            steps{
                script {
                    sh 'docker tag weather_app aviadbarel/weather_app:$BUILD_NUMBER'
                    sh 'docker tag weather_app aviadbarel/weather_app:latest'
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    sh 'docker push aviadbarel/weather_app:$BUILD_NUMBER'
                    sh 'docker push aviadbarel/weather_app:latest'
                }
            }
        }

        stage('Deploy') {
            when{
                branch 'main'
            }
            steps {
                script{
                    sh 'ssh-keyscan -v -H $TARGET_HOST >> ~/.ssh/known_hosts'
//                     sh "scp -i ${SSH_CREDENTIALS_KEY} compose.yml ec2-user@${TARGET_HOST}:/home/ec2-user"
//                     sh "ssh -i ${SSH_CREDENTIALS_KEY} ec2-user@${TARGET_HOST} docker-compose down"
                    sh 'ssh -i $SSH_CREDENTIALS_KEY ec2-user@$TARGET_HOST docker pull aviadbarel/weather_app'
                    sh 'ssh -i $SSH_CREDENTIALS_KEY ec2-user@$TARGET_HOST "docker rm -f weather_app && docker run -d -p 80:8000 --name weather_app aviadbarel/weather_app"'
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
            sh 'docker image rm -f weather_app'
            sh 'docker logout'
            }
    }
}