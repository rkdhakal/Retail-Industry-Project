pipeline {
    agent {
        docker {
            image 'docker:20.10' // Use a Docker image with Docker CLI preinstalled
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        DOCKER_IMAGE = "retail-price-optimizer"
        REPO_URL = "https://github.com/rkdhakal/Retail-Industry-Project"
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

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'docker run --rm $DOCKER_IMAGE pytest tests/'
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    sh 'ansible-playbook -i inventory deploy_model.yml'
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                script {
                    sh 'ansible-playbook -i inventory deploy_model.yml --extra-vars "env=production"'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed.'
        }
    }
}
