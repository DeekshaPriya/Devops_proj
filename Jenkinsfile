pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/DeekshaPriya/Devops_proj.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Flask Docker image...'
                sh 'docker build -t mini-drive-flask ./app'
            }
        }

        stage('Test') {
            steps {
                echo 'Running basic test...'
                sh 'docker run --rm mini-drive-flask python -c "import flask; print(\\"Flask OK\\")"'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying with Docker Compose...'
                sh 'docker compose up -d --build'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Mini Drive is live.'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}