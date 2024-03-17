pipeline {
    agent {node 'agent1'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        SSH_CREDENTIALS_ID = 'Sshdeploy'
        SSH_CREDENTIALS_KEY = credentials("${SSH_CREDENTIALS_ID}")
        TARGET_HOST = '172.31.40.29'
        SNYK_HOME = tool name: 'snyk'
        SONAR_SCANNER_HOME = tool 'SonarCloud'
    }
   
    stages {
        stage('Static analysis') {
            steps{
                withSonarQubeEnv(installationName: 'SonarCloud') {
                    sh """${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.organization=aviad \
                        -Dsonar.projectKey=aviad_weather \
                        -Dsonar.sources=./app \
                        -Dsonar.python.coverage.reportPaths=coverage.xml \
                        -Dsonar.python.xunit.reportPaths=test_results.xml \
                    """                
                }
            }
        }

        stage('OWASP Dependency-Check Vulnerabilities') {
            steps {
                dependencyCheck additionalArguments: '''
                --enableExperimental
                --scan 'app/'
                -f 'ALL'
                --prettyPrint''',
                odcInstallation: 'OWASP',
                nvdCredentialsId: 'NVD',
                stopBuild: true
                
                dependencyCheckPublisher pattern: 'dependency-check-report.xml',
                failedTotalCritical: 1,
                stopBuild: true
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
                    withCredentials([string(credentialsId: 'snyk-api-key', variable: 'TOKEN')]) {
                    sh "${SNYK_HOME}/snyk-linux auth $TOKEN"
                    sh "${SNYK_HOME}/snyk-linux container test weather_app:latest --file=Dockerfile --json-file-output=./snyk.json --severity-threshold=high"
                    }
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

        stage ('Sign image') {
            when{
                branch 'main'
            }
            steps{
                script {
                    sh 'docker trust sign aviadbarel/weather_app:$BUILD_NUMBER'
                    sh 'docker trust sign aviadbarel/weather_app:latest'
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
                    sh 'ssh -i $SSH_CREDENTIALS_KEY ec2-user@$TARGET_HOST "export DOCKER_CONTENT_TRUST=1 | docker pull aviadbarel/weather_app:latest"'
                    sh 'ssh -i $SSH_CREDENTIALS_KEY ec2-user@$TARGET_HOST "docker rm -f weather_app && docker run -d -p 80:8000 --name weather_app aviadbarel/weather_app:latest"'
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
            sh 'docker logout'
            }
    }
}