pipeline {
agent any

```
environment {
    AWS_REGION = "us-east-1"
    ECR_REPO = "538449086740.dkr.ecr.us-east-1.amazonaws.com/siva-elastic-ecr"
    IMAGE_BACKEND = "backend"
    IMAGE_FRONTEND = "frontend"
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
            docker login --username AWS --password-stdin $ECR_REPO
            '''
        }
    }

    stage('Build Backend Image') {
        steps {
            dir('backend') {
                sh '''
                docker build -t $IMAGE_BACKEND .
                docker tag $IMAGE_BACKEND:latest $ECR_REPO:$IMAGE_BACKEND
                '''
            }
        }
    }

    stage('Build Frontend Image') {
        steps {
            dir('frontend') {
                sh '''
                docker build -t $IMAGE_FRONTEND .
                docker tag $IMAGE_FRONTEND:latest $ECR_REPO:$IMAGE_FRONTEND
                '''
            }
        }
    }

    stage('Push Images to ECR') {
        steps {
            sh '''
            docker push $ECR_REPO:$IMAGE_BACKEND
            docker push $ECR_REPO:$IMAGE_FRONTEND
            '''
        }
    }
}
```

}
