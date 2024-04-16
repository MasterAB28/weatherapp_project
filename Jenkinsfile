pipeline {
    agent {node 'agent'}

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub')
        SSH_CREDENTIALS_KEY = credentials('Sshdeploy')
        SNYK_HOME = tool name: 'snyk'
        SONAR_SCANNER_HOME = tool 'SonarCloud'
        IMAGE_NAME = 'weatherapp'
        DOCKER_PASSPHRASE = credentials('DockerPassphrase')
        GITLAB_TOKEN= credentials('gitlab_weather_repo_helm')
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
        stage ('Publish') {
            when{
                branch 'main'
            }
            steps{
                script {
                    sh 'docker tag $IMAGE_NAME aviadbarel/$IMAGE_NAME:V1.$BUILD_NUMBER'
                    sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                    sh 'docker push aviadbarel/$IMAGE_NAME:V1.$BUILD_NUMBER'
                }
            }
        }

        stage ('Sign image') {
            when{
                branch 'main'
            }
            steps{
                script {
                    sh 'echo $DOCKER_PASSPHRASE | docker trust sign aviadbarel/$IMAGE_NAME:V1.$BUILD_NUMBER'
                }
            }
        }

        stage('Deploy') {
            when{
                branch 'main'
            }
            steps {
                script{
                    dir('/home/jenkins/workspace'){

                        sh "git clone http://$GITLAB_TOKEN@172.31.35.116/root/weather_app_helm.git"
                        dir('/home/jenkins/workspace/weather_app_helm'){
                            sh 'chmod +x ./version.sh'
                            sh "./version.sh $BUILD_NUMBER"

                            sh 'git add .'
                            sh 'git config --global user.email aviad0909@gmail.com'
                            sh 'git config --global user.name Aviad'
                            sh 'git commit -m "JenkinsAction: Update Docker image tag"'
                            sh 'git push'
                        }
                    }
                }
            }
        }
    } // Close stages block

    post {
        success{
            slackSend(channel: 'succeeded-build', color: 'good', message: "Tests passed! build: ${BUILD_NUMBER} commit: ${GIT_COMMIT}")
        }
        failure{
            slackSend(channel: 'devops-alert', color: 'danger', message: "Tests failed! ${BUILD_NUMBER} commit: ${GIT_COMMIT}")
        }
        always {
            cleanWs()
            sh 'docker logout'
        }
    } // Close post block
} // Close pipeline block
