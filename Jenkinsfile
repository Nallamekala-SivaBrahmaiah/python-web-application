pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'sonar-qube' // Name of your SonarQube server in Jenkins
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
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install --upgrade pip'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pip install pytest pytest-cov'
                sh '. venv/bin/activate && pytest --cov=. --cov-report=xml'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(SONARQUBE_SERVER) {
                    sh ". venv/bin/activate && sonar-scanner \
                        -Dsonar.login=${SONARQUBE_TOKEN}"
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
