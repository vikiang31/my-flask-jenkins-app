pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh 'chmod +x scripts/run_checks.sh'
                sh './scripts/run_checks.sh'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-flask-jenkins-app:latest .'
            }
        }
    }

    post {
        success {
            echo 'Pipeline finished successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
