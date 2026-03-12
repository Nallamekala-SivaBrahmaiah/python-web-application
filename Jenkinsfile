pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'sonar-qube'
        SONARQUBE_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                // Install venv if not already installed (Debian/Ubuntu agents)
                sh '''
                    sudo apt update || true
                    sudo apt install -y python3-venv python3-pip || true
                '''
            }
        }

        stage('Checkout') {
            steps {
                git url: 'https://github.com/Nallamekala-SivaBrahmaiah/python-web-application.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
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
