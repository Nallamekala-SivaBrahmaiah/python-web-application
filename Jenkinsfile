pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO = "538449086740.dkr.ecr.us-east-1.amazonaws.com/siva-elastic-ecr"
        ECR_REGISTRY = "538449086740.dkr.ecr.us-east-1.amazonaws.com"
        SONARQUBE_SERVER = "SonarQube" // Name of your Jenkins SonarQube server
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Nallamekala-SivaBrahmaiah/python-web-application.git'
            }
        }

        stage('SonarQube Analysis') {
            environment {
                SONAR_AUTH_TOKEN = credentials('sonar-token') // Jenkins credential with your SonarQube token
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                    sonar-scanner \
                      -Dsonar.projectKey=python-web-app \
                      -Dsonar.sources=. \
                      -Dsonar.tests=tests \
                      -Dsonar.python.version=3.11 \
                      -Dsonar.sourceEncoding=UTF-8 \
                      -Dsonar.python.coverage.reportPaths=coverage.xml \
                      -Dsonar.exclusions=**/venv/**,**/__pycache__/**,**/migrations/**,**/docs/**,**/*.md,**/*.txt \
                      -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
                '''
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                docker build -t $ECR_REPO:backend ./backend
                docker build -t $ECR_REPO:frontend ./frontend
                '''
            }
        }

        stage('Push Images') {
            steps {
                sh '''
                docker push $ECR_REPO:backend
                docker push $ECR_REPO:frontend
                '''
            }
        }
    }
}
