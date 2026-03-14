pipeline {
    agent any

environment {
    AWS_REGION = "us-east-2"
    ECR_REPO = "538449086740.dkr.ecr.us-east-2.amazonaws.com/siva-awscloud"
    ECR_REGISTRY = "538449086740.dkr.ecr.us-east-2.amazonaws.com"
    IMAGE_TAG = "${BUILD_NUMBER}"
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
            aws ecr get-login-password --region $AWS_REGION \
            | docker login --username AWS --password-stdin $ECR_REGISTRY
            '''
        }
    }

    stage('Build Docker Images') {
        steps {
            sh '''
            docker build -t $ECR_REPO:backend-$IMAGE_TAG backend
            docker build -t $ECR_REPO:frontend-$IMAGE_TAG frontend
            '''
        }
    }

    stage('Push Images to ECR') {
        steps {
            sh '''
            docker push $ECR_REPO:backend-$IMAGE_TAG
            docker push $ECR_REPO:frontend-$IMAGE_TAG
            '''
        }
    }

    stage('Trivy Security Scan') {
        steps {
            sh '''
            echo "Scanning backend image..."
            trivy image --severity HIGH,CRITICAL $ECR_REPO:backend-$IMAGE_TAG || true

            echo "Scanning frontend image..."
            trivy image --severity HIGH,CRITICAL $ECR_REPO:frontend-$IMAGE_TAG || true
            '''
        }
    }

    stage('Deploy to Kubernetes') {
        steps {
            sh '''
            kubectl apply -f mayabazar-k8s.yaml
            '''
        }
    }
}

}
