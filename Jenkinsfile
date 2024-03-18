pipeline {
    agent {node 'agent'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        SSH_CREDENTIALS_KEY = credentials('Sshdeploy')
        TARGET_HOST = '172.31.40.29'
        SNYK_HOME = tool name: 'snyk'
        SONAR_SCANNER_HOME = tool 'SonarCloud'
        IMAGE_NAME = 'weatherapp'
        DOCKER_PASSPHRASE = credentials('DockerPassphrase')
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
                    sh 'docker build . -t $IMAGE_NAME'
                }
            }
        }
        stage('Tests') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'snyk-api-key', variable: 'TOKEN')]) {
                        sh '$SNYK_HOME/snyk-linux auth $TOKEN'
                        sh '$SNYK_HOME/snyk-linux container test $IMAGE_NAME:latest --file=Dockerfile --json-file-output=./snyk.json --severity-threshold=high'
                    }
                    // Run tests
                    sh 'docker run -d -p 80:8000 --name test $IMAGE_NAME '
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
                    sh 'docker tag $IMAGE_NAME aviadbarel/$IMAGE_NAME:$BUILD_NUMBER'
                    sh 'docker tag $IMAGE_NAME aviadbarel/$IMAGE_NAME:latest'
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    sh 'docker push aviadbarel/$IMAGE_NAME:$BUILD_NUMBER'
                    sh 'docker push aviadbarel/$IMAGE_NAME:latest'
                }
            }
        }

        stage ('Sign image') {
            when{
                branch 'main'
            }
            steps{
                script {
                    sh 'echo "av280800" | docker trust sign aviadbarel/$IMAGE_NAME:$BUILD_NUMBER'
                    sh 'echo "av280800" | docker trust sign aviadbarel/$IMAGE_NAME:latest'
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

                    sh 'ssh -i $SSH_CREDENTIALS_KEY ec2-user@$TARGET_HOST "export DOCKER_CONTENT_TRUST=1 && docker pull aviadbarel/$IMAGE_NAME:latest"'
                    sh 'ssh -i $SSH_CREDENTIALS_KEY ec2-user@$TARGET_HOST "docker rm -f $IMAGE_NAME && docker run -d -p 80:8000 --name $IMAGE_NAME aviadbarel/$IMAGE_NAME:latest"'
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