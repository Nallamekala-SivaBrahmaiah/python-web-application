pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO = "538449086740.dkr.ecr.us-east-1.amazonaws.com/siva-elastic-ecr"
        ECR_REGISTRY = "538449086740.dkr.ecr.us-east-1.amazonaws.com"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Nallamekala-SivaBrahmaiah/python-web-application.git'
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
