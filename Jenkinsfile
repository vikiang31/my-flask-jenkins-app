pipeline {
    agent any

    environment {
        LOCAL_IMAGE = 'my-flask-jenkins-app:latest'
        REMOTE_IMAGE = 'vikiang31/my-flask-jenkins-app:latest'
    }

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
                sh 'docker build -t $LOCAL_IMAGE .'
                sh 'docker tag $LOCAL_IMAGE $REMOTE_IMAGE'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push $REMOTE_IMAGE'
                }
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
        always {
            sh 'docker logout || true'
        }
    }
}
