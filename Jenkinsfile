pipeline {
    agent {
        docker {
            image 'docker:24.0.7' // Ensure this matches your Docker version
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock -v $WORKSPACE/.docker:/root/.docker'
        }
    }

    environment {
        DOCKER_IMAGE = "retail-price-optimizer"
        REPO_URL = "https://github.com/rkdhakal/Retail-Industry-Project"
        DOCKER_CONFIG = "$WORKSPACE/.docker" // Ensure Docker uses this configuration directory
        SANITIZED_WORKSPACE = "${WORKSPACE.replaceAll(' ', '_').toLowerCase()}" // Replace spaces with underscores
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
                    docker info
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
            docker run --rm -v "$WORKSPACE:/app" -w /app -v "$DOCKER_CONFIG:/root/.docker" $DOCKER_IMAGE \
                bash -c "ansible-playbook -i ansible/inventory ansible/deploy_model.yml"
        '''
    }
}


        stage('Deploy to Production') {
            steps {
                sh '''
                    echo "Deploying to Production..."
                    docker run --rm -v "$WORKSPACE:/app" -w /app -v "$DOCKER_CONFIG:/root/.docker" $DOCKER_IMAGE \
                        bash -c "apt-get update && apt-get install -y ansible && \
                        ansible-playbook -i ansible/inventory ansible/deploy_model.yml --extra-vars 'env=production'"
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
