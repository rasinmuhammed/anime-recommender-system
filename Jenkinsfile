pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'vast-art-454104-f1'
        GCLOUD_PATH = 'car/jenkins_home/googgle-cloud-sdk/bin'
        KUBECTL_AUTH_PLUGIN = '/usr/lib/google-cloud-sdk/bin'
    }

    stages {
        stage("Cloning from Github"){
            steps{
                script {
                    echo "Cloning from Github"
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/rasinmuhammed/anime-recommender-system.git']])
                }
            }
        }

        stage("Making a virtual environment"){
            steps{
                script {
                    echo "Making a virtual environment"

                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                   
                }
            }
        }

        stage('DVC Pull'){
            steps{
                withCredentials([file(crendentialsId: 'gcp-key2', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Pulling data from DVC"
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }

        stage('Build and Push Docker Image to GCR'){
            steps{
                withCredentials([file(crendentialsId: 'gcp-key2', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Build and Push Docker Image to GCR"
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker
                        docker build -t gcr.io/${GCP_PROJECT}/anime-recommender-system:latest .
                        docker push gcr.io/${GCP_PROJECT}/anime-recommender-system:latest
                        '''
                    }
                }
            }
        }

        stage('Deploying to Kubernetes'){
            steps{
                withCredentials([file(crendentialsId: 'gcp-key2', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Deploying to Kubernetes'"
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}: ${KUBECTL_AUTH_PLUGIN}
                        gloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-app-cluster --zone us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }

}