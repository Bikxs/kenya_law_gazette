# Build the Docker image
docker build -t kenya-law-gazette-frontend .

# Tag the image
docker tag kenya-law-gazette-frontend:latest 851725533694.dkr.ecr.us-east-1.amazonaws.com/kenya-law-gazette/frontend:latest

# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 851725533694.dkr.ecr.us-east-1.amazonaws.com

# Push the image to ECR
docker push 851725533694.dkr.ecr.us-east-1.amazonaws.com/kenya-law-gazette/frontend:latest
