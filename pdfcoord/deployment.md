### Deployment Guide for Django Web Application on AWS
This guide provides detailed steps for deploying the Django web application to AWS EC2, utilizing S3 for static and media files, and configuring a MySQL database using AWS RDS.

## Prerequisites
AWS account
Basic knowledge of AWS services (EC2, RDS, S3)
SSH client installed
Git installed
Local Django project ready for deployment
## 1. Set Up AWS RDS for MySQL
Create RDS Instance:

Go to the RDS dashboard in your AWS Management Console.
Click Create database and select MySQL.
Configure the database settings (instance size, storage, username, password).
Set the database name, security groups, and make sure the instance is publicly accessible if required.
Security Groups:

Update the security group of your RDS instance to allow traffic on port 3306 from your EC2 instance's security group.
## 2. Prepare Your Django Application
Configure Django for Production:

Update DATABASES configuration in your settings.py to use the RDS endpoint.
Ensure DEBUG is set to False.
Configure ALLOWED_HOSTS with your EC2 public IP or domain name.
Static and Media Files:

Install boto3 and django-storages via pip.
Update settings.py to configure S3 buckets for handling static and media files.
Dependencies:

Create a requirements.txt file using pip freeze > requirements.txt.
## 3. Deploy to AWS EC2
Launch EC2 Instance:

Choose an Amazon Machine Image (AMI), e.g., Ubuntu Server.
Configure instance details, add storage, and set security groups that open ports 22 (SSH), 80 (HTTP), and 443 (HTTPS).
Launch the instance and download the key pair.
SSH into Your Instance:

Use the downloaded key pair to SSH into your instance: ssh -i "your-key.pem" ubuntu@your-ec2-public-ip-address.
Server Setup:

Update packages: sudo apt-get update.
Install Python, pip, and other necessary packages: sudo apt-get install python3-pip python3-dev libmysqlclient-dev.
Install a web server, e.g., Nginx, and configure it to serve your Django app.
Deploy The Django App:

Clone the repository or transfer the project files to the EC2 instance.
cd to the production/pdfcoord
Install dependencies from requirements.txt.
Run migrations and collect static files: python manage.py migrate and python manage.py collectstatic.
## 4. Configure S3 Buckets
Create S3 Buckets:

Go to the S3 management console.
Create new buckets for static and media files, ensuring they are set for public access if necessary.
Update Django Settings:

Configure AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY.
## 5. Final Steps
Ensure all environment variables are set properly, including database credentials and secret keys.
Restart the web server to apply all changes: sudo systemctl restart nginx.
Verify that the application is running by accessing your EC2 instance's public IP or domain in a browser.