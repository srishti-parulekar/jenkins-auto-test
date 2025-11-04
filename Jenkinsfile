pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Test in Python Container') {
            agent {
                docker {
                    image 'python:3.9-slim'
                    reuseNode true
                }
            }
            steps {
                sh '''
                    pip install -r requirements.txt
                    mkdir -p reports
                    pytest -v --cov=. --cov-report=html --cov-report=xml --junitxml=reports/junit.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                    publishHTML([
                        allowMissing: true,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("smartcalc-service:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Test Docker Image') {
            steps {
                sh "docker run --rm smartcalc-service:${env.BUILD_ID} python -c 'from app import SmartCalc; calc = SmartCalc(); print(\"Docker test: 2 + 3 =\", calc.add(2, 3)); print(\"Docker test: 10 / 2 =\", calc.divide(10, 2))'"
            }
        }
    }
    
    post {
        always {
            echo "Build ${currentBuild.result} - ${currentBuild.fullDisplayName}"
            cleanWs()
        }
        success {
            echo "🎉 All tests passed! SmartCalc service is ready."
        }
        failure {
            echo "❌ Build failed! Check test results."
        }
    }
}