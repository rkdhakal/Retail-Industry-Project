pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "retail-price-optimizer" // Docker image name
        REPO_URL = "https://github.com/rkdhakal/Retail-Industry-Project"
        GIT_CREDENTIALS = "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" // Set up your GitHub PAT in Jenkins credentials
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm: [
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    submoduleCfg: [],
                    userRemoteConfigs: [[
                        credentialsId: "${GIT_CREDENTIALS}",
                        url: "${REPO_URL}"
                    ]]
                ]
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
