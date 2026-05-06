pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/DeekshaPriya/Devops_proj.git'
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
                echo 'Deploying container...'
                sh 'docker run -d -p 5000:5000 --name mini-drive-app mini-drive-flask'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Mini Drive is live.'
        }
        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}