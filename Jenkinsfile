pipeline {
agent any

```
environment {
    AWS_REGION = "us-east-1"
    ECR_REPO = "538449086740.dkr.ecr.us-east-1.amazonaws.com/siva-elastic-ecr"
}

stages {

    stage('Clone Repository') {
        steps {
            git branch: 'main',
            url: 'https://github.com/Nallamekala-SivaBrahmaiah/python-web-application.git'
        }
    }

    stage('Login to AWS ECR') {
        steps {
            sh '''
            aws ecr get-login-password --region $AWS_REGION | \
            docker login --username AWS --password-stdin 538449086740.dkr.ecr.us-east-1.amazonaws.com
            '''
        }
    }

    stage('Build Backend Image') {
        steps {
            dir('backend') {
                sh '''
                docker build -t backend .
                docker tag backend:latest $ECR_REPO:backend
                '''
            }
        }
    }

    stage('Build Frontend Image') {
        steps {
            dir('frontend') {
                sh '''
                docker build -t frontend .
                docker tag frontend:latest $ECR_REPO:frontend
                '''
            }
        }
    }

    stage('Push Images to ECR') {
        steps {
            sh '''
            docker push $ECR_REPO:backend
            docker push $ECR_REPO:frontend
            '''
        }
    }

}
```

}
