pipeline {
    agent {
        docker {
            image 'docker:latest' // Use a Docker image with Docker CLI preinstalled
            args '--privileged -v /var/run/docker.sock:/var/run/docker.sock' // Mount Docker socket
        }
    }

    environment {
        DOCKER_IMAGE = "retail-price-optimizer" // Name of your Docker image
        REPO_URL = "https://github.com/rkdhakal/Retail-Industry-Project" // Repository URL
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    // Use Jenkins credentials to securely access the repository
                    withCredentials([string(credentialsId: 'github_pat_credentials', variable: 'GIT_PAT')]) {
                        checkout scm: [
                            $class: 'GitSCM',
                            branches: [[name: '*/main']],
                            doGenerateSubmoduleConfigurations: false,
                            extensions: [],
                            userRemoteConfigs: [[
                                url: "https://${GIT_PAT}@github.com/rkdhakal/Retail-Industry-Project"
                            ]]
                        ]
                    }
                }
            }
        }

        stage('Prepare Docker Access') {
            steps {
                script {
                    // Ensure the Jenkins user can access Docker socket
                    sh 'sudo chmod 666 /var/run/docker.sock'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run tests inside the Docker container
                    sh 'docker run --rm $DOCKER_IMAGE pytest tests/'
                }
            }
        }

        stage('Deploy to Staging') {
            steps {
                script {
                    // Use Ansible to deploy the application to staging
                    sh 'ansible-playbook -i inventory deploy_model.yml'
                }
            }
        }

        stage('User Acceptance Testing (UAT)') {
            steps {
                echo 'Notify stakeholders for UAT'
            }
        }

        stage('Deploy to Production') {
            steps {
                script {
                    // Deploy to production with Ansible
                    sh 'ansible-playbook -i inventory deploy_model.yml --extra-vars "env=production"'
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/test-results.xml', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline execution failed.'
        }
    }
}
