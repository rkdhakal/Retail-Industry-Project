pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "retail-price-optimizer" // Docker image name
        REPO_URL = "https://github.com/rkdhakal/Retail-Industry-Project"
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    // Use Jenkins credentials for secure access
                       withCredentials([string(credentialsId: 'github_pat_credentials', variable: 'GIT_PAT')]) {
                            checkout scm: [
                            $class: 'GitSCM',
                            branches: [[name: '*/main']],
                            doGenerateSubmoduleConfigurations: false,
                            extensions: [],
                            submoduleCfg: [],
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

        stage('User Acceptance Testing (UAT)') {
            steps {
                echo 'Notify stakeholders for UAT'
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
