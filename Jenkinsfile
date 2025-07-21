pipeline {
    agent any

    environment {
        dockerImage = "thapavishal/elearning"
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                git url: 'https://github.com/ithapavishal/django-cicd.git', branch: 'django-pipeline'
            }
        }

        stage('Build Django App Image') {
            // agent {
            //     label 'ubuntu-pipeline-slave-node'
            // }
            steps {
                sh 'docker build -t $dockerImage:$BUILD_NUMBER .'
            }
        }

        stage('Push Image to DockerHub') {
            // agent {
            //     label 'ubuntu-pipeline-slave-node'
            // }
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-credentials', url: '']) {
                    sh 'docker push $dockerImage:$BUILD_NUMBER'
                }
            }
        }

        stage('Deploy to Development') {
            // agent {
            //     label 'ubuntu-pipeline-slave-node'
            // }
            steps {
                echo 'Deploying to development via Ansible'
                sh '''
                ansible-playbook -i inventory deploy.yaml --extra-vars "env=dev image_tag=$dockerImage:$BUILD_NUMBER"
                '''
            }
        }

        stage('Deploy to Production') {
            // agent {
            //     label 'ubuntu-pipeline-slave-node'
            // }
            steps {
                timeout(time: 1, unit: 'DAYS') {
                    input id: 'confirm', message: 'Approve deployment to production environment?'
                }
                echo 'Deploying to production via Ansible'
                sh '''
                ansible-playbook -i inventory deploy.yaml --extra-vars "env=prod image_tag=$dockerImage:$BUILD_NUMBER"
                '''
            }
        }
    }

    post {
        always {
            mail to: 'v01.thapa@gmail.com',
                subject: "Job '${JOB_NAME}' (${BUILD_NUMBER}) status",
                body: "Go to ${BUILD_URL} and verify the build"
        }
        success {
            mail body: """Hi Team,
Build #$BUILD_NUMBER succeeded. Visit:
$BUILD_URL
Regards,
DevOps Team""",
            subject: 'BUILD SUCCESS NOTIFICATION',
            to: 'v01.thapa@gmail.com'
        }
        failure {
            mail body: """Hi Team,
Build #$BUILD_NUMBER failed. Visit:
$BUILD_URL
Regards,
DevOps Team""",
            subject: 'BUILD FAILED NOTIFICATION',
            to: 'v01.thapa@gmail.com'
        }
    }
}
