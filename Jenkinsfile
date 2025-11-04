pipeline {
    agent {
        docker {
            image 'python:3.9-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pip list
                '''
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh '''
                    echo "Running unit tests..."
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
                sh '''
                    docker run --rm smartcalc-service:${BUILD_ID} python -c "
                    from app import SmartCalc
                    calc = SmartCalc()
                    print('Docker test: 2 + 3 =', calc.add(2, 3))
                    print('Docker test: 10 / 2 =', calc.divide(10, 2))
                    "
                '''
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
            emailext (
                subject: "SUCCESS: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "The SmartCalc service build #${env.BUILD_NUMBER} passed all tests.",
                to: "developer@example.com"
            )
        }
        failure {
            echo "❌ Build failed! Check test results."
            emailext (
                subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "The SmartCalc service build #${env.BUILD_NUMBER} failed. Please check Jenkins.",
                to: "developer@example.com"
            )
        }
    }
}
