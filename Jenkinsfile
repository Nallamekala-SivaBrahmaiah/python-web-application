pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        ECR_REPO = "538449086740.dkr.ecr.us-east-1.amazonaws.com/siva-elastic-ecr"
        ECR_REGISTRY = "538449086740.dkr.ecr.us-east-1.amazonaws.com"
        SONAR_HOST_URL = "http://your-sonarqube-server:9000"  // Update with your SonarQube URL
        SONAR_PROJECT_KEY = "python-web-app"  // Choose a unique key for your project
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/Nallamekala-SivaBrahmaiah/python-web-application.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Create sonar-project.properties file
                    writeFile file: 'sonar-project.properties', text: """
                        sonar.projectKey=${SONAR_PROJECT_KEY}
                        sonar.projectName=Python Web Application
                        sonar.projectVersion=1.0
                        sonar.sources=.
                        sonar.sourceEncoding=UTF-8
                        sonar.language=py
                        sonar.exclusions=**/venv/**, **/__pycache__/**, **/*.pyc
                        sonar.python.coverage.reportPaths=coverage.xml
                        sonar.python.xunit.reportPath=test-results.xml
                    """
                    
                    // Run SonarQube analysis
                    withSonarQubeEnv('SonarQube') {  // Use the name configured in Jenkins
                        sh '''
                            sonar-scanner \
                                -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=${SONAR_HOST_URL}
                        '''
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    timeout(time: 5, unit: 'MINUTES') {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to quality gate failure: ${qg.status}"
                        }
                    }
                }
            }
        }

        stage('Run Tests & Coverage') {
            steps {
                sh '''
                    # Install dependencies
                    pip install pytest pytest-cov
                    
                    # Run tests with coverage
                    pytest --cov=. --cov-report=xml:coverage.xml --junitxml=test-results.xml
                '''
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
