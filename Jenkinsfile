pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'sonar-qube' // Jenkins SonarQube server name
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
                    # Create virtual environment
                    python3 -m venv venv

                    # Activate virtual environment
                    . venv/bin/activate

                    # Upgrade pip and install dependencies
                    pip install --upgrade pip
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi

                    # Install testing tools
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

    post {
        always {
            echo 'Cleaning up virtual environment...'
            sh 'rm -rf venv'
        }
    }
}
