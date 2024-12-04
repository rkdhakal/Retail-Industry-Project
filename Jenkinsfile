pipeline {
    agent {
        docker {
            image 'docker:24.0.7' // Use the appropriate Docker image version
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock' // Ensure privileged access
        }
    }

    environment {
        DOCKER_IMAGE = "retail-price-optimizer" // Docker image to be built
        REPO_URL = "https://github.com/rkdhakal/Retail-Industry-Project" // GitHub repository
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'github_pat_credentials', variable: 'GIT_PAT')]) {
                        checkout scm: [
                            $class: 'GitSCM',
                            branches: [[name: '*/main']],
                            userRemoteConfigs: [[
                                url: "https://${GIT_PAT}@github.com/rkdhakal/Retail-Industry-Project"
                            ]]
                        ]
                    }
                }
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

        stage('Run Tests') {
            steps {
                sh '''
                    echo "Running Tests..."
                    docker run --rm $DOCKER_IMAGE pytest tests/
                '''
            }
        }

        stage('Deploy to Staging') {
            steps {
                sh '''
                    echo "Deploying to Staging..."
                    ansible-playbook -i inventory deploy_model.yml
                '''
            }
        }

        stage('Deploy to Production') {
            steps {
                sh '''
                    echo "Deploying to Production..."
                    ansible-playbook -i inventory deploy_model.yml --extra-vars "env=production"
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
