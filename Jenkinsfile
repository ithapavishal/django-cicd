pipeline {
    agent any

    environment {
        dockerImage = "thapavishal/elearning"
        ANSIBLE_CONFIG = "${WORKSPACE}/ansible.cfg"
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                sh '''
                echo "[defaults]" > ansible.cfg
                echo "host_key_checking = False" >> ansible.cfg
                echo "remote_user = vagrant" >> ansible.cfg
                echo "private_key_file = /var/lib/jenkins/.ssh/id_rsa" >> ansible.cfg
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $dockerImage:$BUILD_NUMBER .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withDockerRegistry([credentialsId: 'dockerhub-credentials', url: '']) {
                    sh 'docker push $dockerImage:$BUILD_NUMBER'
                }
            }
        }

        stage('Deploy to Development') {
            steps {
                sshagent(credentials: ['vagrant-ssh-key']) {
                    sh '''
                    ansible-playbook -i inventory deploy.yaml \
                      --extra-vars "env=dev image_tag=$dockerImage:$BUILD_NUMBER"
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                timeout(time: 1, unit: 'DAYS') {
                    input message: 'Approve production deployment?'
                }
                sshagent(credentials: ['vagrant-ssh-key']) {
                    sh '''
                    ansible-playbook -i inventory deploy.yaml \
                      --extra-vars "env=prod image_tag=$dockerImage:$BUILD_NUMBER"
                    '''
                }
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
