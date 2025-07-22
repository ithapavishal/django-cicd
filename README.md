# Django CI/CD Pipeline with Docker, Jenkins, and Ansible

This project demonstrates a complete CI/CD pipeline for a Django application using:
- Docker for containerization
- Jenkins for automation
- Ansible for deployment
- Vagrant for local development environment

## Prerequisites

- Vagrant 2.2+
- VirtualBox 6.0+
- Git

Infrastructure Setup

1. Start Vagrant Machines
```bash
vagrant up
This creates three virtual machines:

Jenkins server (192.168.56.10)
Development server (192.168.56.20)
Production server (192.168.56.30)

Configuration Steps

2. Configure SSH Access

On Jenkins Server:
vagrant ssh jenkins
sudo su - jenkins
ssh-keygen -t rsa -b 4096 -m PEM -f ~/.ssh/id_rsa -N ""
chmod 600 ~/.ssh/id_rsa

Copy keys to target servers: 
ssh-copy-id -i ~/.ssh/id_rsa.pub vagrant@192.168.56.20
ssh-copy-id -i ~/.ssh/id_rsa.pub vagrant@192.168.56.30
# Password: vagrant

3. Configure Target Servers

On both dev and prod servers:

bash
vagrant ssh dev  # or vagrant ssh prod
sudo nano /etc/ssh/sshd_config

Ensure these settings:

PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PasswordAuthentication no  # Set to 'yes' temporarily if needed

Restart SSH:

sudo systemctl restart sshd

4. Jenkins Setup

i. Access Jenkins at: http://192.168.56.10:8080
ii. Install required plugins:
Docker Pipeline
Ansible
SSH Agent
iii. Add credentials:
Docker Hub credentials (ID: dockerhub-credentials)
SSH key (ID: vagrant-ssh-key) - Paste contents of /var/lib/jenkins/.ssh/id_rsa

Pipeline Workflow

The Jenkins pipeline performs these steps:

Checks out code from GitHub
Builds Docker image
Pushes image to Docker Hub
Deploys to development server
After approval, deploys to production


File Structure

.
├── Dockerfile              # Docker configuration
├── Jenkinsfile            # Pipeline definition
├── deploy.yaml            # Ansible playbook
├── inventory              # Server inventory
├── requirements.txt       # Python dependencies
└── (Django project files)

Troubleshooting ;

SSH Connection Issues

Verify keys exist:
sudo su - jenkins
ls -la ~/.ssh/

Check authentication logs on target servers:
sudo tail -f /var/log/auth.log

Test connection manually:
ssh -v -i ~/.ssh/id_rsa vagrant@192.168.56.20

Permission Denied Errors

Ensure correct permissions:

chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 600 ~/.ssh/authorized_keys  # On target servers

N.B. Important Notes

The Jenkins user (/var/lib/jenkins) owns the SSH keys, not the vagrant user
All deployment operations run as the Jenkins user
For security, keep PasswordAuthentication no after setup is complete

