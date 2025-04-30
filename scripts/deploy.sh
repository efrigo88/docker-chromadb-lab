#!/bin/bash

# Exit on error
set -e

# Source environment variables
source .env

# Export AWS credentials from .env
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION

# Initialize and apply Terraform
cd infra
terraform init
terraform apply -auto-approve

# Configuration
AWS_REGION=${AWS_DEFAULT_REGION:-$(aws configure get region)}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPOSITORY="data-pipeline"
IMAGE_TAG="latest"

echo "🚀 Starting deployment process..."

# Build Docker image
echo "📦 Building Docker image..."
cd ..
docker buildx build --platform linux/amd64 -t ${ECR_REPOSITORY}:${IMAGE_TAG} .

# Login to ECR
echo "🔑 Logging in to ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# Tag and push Docker image
echo "🏷️  Tagging and pushing Docker image..."
docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_TAG}
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}:${IMAGE_TAG}

echo "✅ Deployment completed successfully!"

# Get Terraform outputs
cd infra
SUBNET_ID=$(terraform output -json subnet_ids | jq -r '.[0]')
SECURITY_GROUP_ID=$(terraform output -raw security_group_id)
TASK_DEFINITION_ARN=$(terraform output -raw task_definition_arn)
cd ..

# Instructions for running ECS task
echo "
📋 To run the ECS task, use the following command:

aws ecs run-task \\
  --region ${AWS_REGION} \\
  --cluster data-pipeline-cluster \\
  --task-definition ${TASK_DEFINITION_ARN} \\
  --launch-type FARGATE \\
  --network-configuration \"awsvpcConfiguration={subnets=[${SUBNET_ID}],securityGroups=[${SECURITY_GROUP_ID}],assignPublicIp=ENABLED}\"

📋 To monitor the task status, use:

aws ecs describe-tasks --cluster data-pipeline-cluster --tasks <task-id>

Note: Replace <task-id> with the task ID from the run-task command output.
"
