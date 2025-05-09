pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'vast-art-454104-f1'
        GCLOUD_PATH = 'car/jenkins_home/googgle-cloud-sdk/bin'
        KUBECTL_AUTH_PLUGIN = '/usr/lib/google-cloud-sdk/bin'
        DOCKER_BUILDKIT = '1' // Enable BuildKit for more efficient builds
        DOCKER_IMAGE_NAME = "gcr.io/${GCP_PROJECT}/anime-recommender-system"
    }

    options {
        // Limit builds kept in history to save disk space
        buildDiscarder(logRotator(numToKeepStr: '5'))
        // Skip default checkout to control it ourselves
        skipDefaultCheckout(true)
    }

    stages {
        stage("Cleanup Workspace") {
            steps {
                script {
                    echo "Cleaning workspace"
                    cleanWs()
                }
            }
        }

        stage("Cloning from Github") {
            steps {
                script {
                    echo "Cloning from Github"
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        extensions: [[$class: 'CloneOption', depth: 1, noTags: true, shallow: true]],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/rasinmuhammed/anime-recommender-system.git'
                        ]]
                    ])
                }
            }
        }

        stage("Making a virtual environment") {
            steps {
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

        stage("Pull Only Required DVC Files") {
            steps {
                withCredentials([file(credentialsId: 'gcp-key2', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Pulling only required data from DVC"
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        
                        # Pull only the model and weights (not the raw data)
                        dvc pull artifacts/model.dvc artifacts/weights.dvc
                        '''
                    }
                }
            }
        }

        stage("Build and Push Docker Image to GCR") {
            steps {
                withCredentials([file(credentialsId: 'gcp-key2', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Build and Push Docker Image to GCR with cache optimization"
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker

                        # Use Docker BuildKit cache
                        docker buildx create --use || true
                        
                        # Build with cache from previous builds & optimize for push
                        docker buildx build --platform=linux/amd64 \
                            --cache-from=${DOCKER_IMAGE_NAME}:latest \
                            --build-arg BUILDKIT_INLINE_CACHE=1 \
                            -t ${DOCKER_IMAGE_NAME}:latest \
                            -t ${DOCKER_IMAGE_NAME}:${BUILD_NUMBER} \
                            --push .
                        '''
                    }
                }
            }
        }

        stage("Deploying to Kubernetes") {
            steps {
                withCredentials([file(credentialsId: 'gcp-key2', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo "Deploying to Kubernetes"
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-app-cluster --zone us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs(cleanWhenNotBuilt: true,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true)
            
            sh 'docker system prune -f || true'
        }
    }
}