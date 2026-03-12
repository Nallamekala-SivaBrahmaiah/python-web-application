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
        
        stage('Maven Build') {
            steps {
                sh 'mvn package'
            }
        }
        
        stage('SonarQube Code Scan') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh '''
                    mvn sonar:sonar \
                    -Dsonar.projectKey=java-web-application \
                    -Dsonar.sources=backend,frontend,src
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
        
        stage('Trivy Scan Images') {
            steps {
                sh '''
                echo "Scanning backend image..."
                trivy image --severity HIGH,CRITICAL $ECR_REPO:backend || true
                echo "Scanning frontend image..."
                trivy image --severity HIGH,CRITICAL $ECR_REPO:frontend || true
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
            
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f jenkins.yaml
                '''
            }
        }
    }
}
