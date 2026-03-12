pipeline {
    agent {
        docker { image 'python:3.12-slim' } // Python environment guaranteed
    }

    environment {
        SONARQUBE_SERVER = 'sonar-qube' // Your SonarQube server in Jenkins
        SONARQUBE_TOKEN = credentials('sonar-token') // Jenkins credential ID for Sonar token
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/Nallamekala-SivaBrahmaiah/python-web-application.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest --cov=. --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(SONARQUBE_SERVER) {
                    sh '''
                        . venv/bin/activate
                        sonar-scanner -Dsonar.login=${SONARQUBE_TOKEN}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}
