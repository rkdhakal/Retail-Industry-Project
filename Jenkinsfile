pipeline {
    agent {
        docker {
            image 'docker:24.0.7'
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock -v $WORKSPACE/.docker:/root/.docker'
        }
    }

    environment {
        DOCKER_IMAGE = "retail-price-optimizer"
        REPO_URL = "https://github.com/rkdhakal/Retail-Industry-Project"
        DOCKER_CONFIG = "$WORKSPACE/.docker"
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Verify Docker Access') {
            steps {
                sh '''
                    echo "Verifying Docker Access..."
                    docker info || echo "Docker daemon is not accessible"
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker Image..."
                    docker build -t $DOCKER_IMAGE .
                '''
            }
        }
        
        stage('Deploy to Staging') {
            steps {
                sh '''
                    echo "Deploying to Staging..."
                    docker rm -f retail-pricing-system || echo "No existing container to remove"
                    docker run -d --name retail-pricing-system -p 8501:8501 retail-price-optimizer
                '''
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                    echo "Deploying to Production..."
                    docker rm -f retail-pricing-system-production || echo "No existing production container to remove"
                    docker run -d --name retail-pricing-system-production -p 8502:8501 retail-price-optimizer \
                        bash -c "ansible-playbook -i ansible/inventory ansible/deploy_model.yml --extra-vars 'env=production'"
                '''
            }
        }
        
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed. Check the logs for details.'
        }
    }
}
