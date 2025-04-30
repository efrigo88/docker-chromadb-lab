#!/bin/bash

# Exit on error
set -e

# Source environment variables
source .env

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

# Instructions for running ECS task
echo "
📋 To run the ECS task, use the following command:

aws ecs run-task \\
  --cluster data-pipeline-cluster \\
  --task-definition \$(terraform output -raw task_definition_arn) \\
  --launch-type FARGATE \\
  --network-configuration \"awsvpcConfiguration={subnets=[\$(terraform output -raw subnet_ids | jq -r '.[0]')],securityGroups=[\$(terraform output -raw security_group_id)],assignPublicIp=ENABLED}\"

📋 To monitor the task status, use:

aws ecs describe-tasks --cluster data-pipeline-cluster --tasks <task-id>

Note: Replace <task-id> with the task ID from the run-task command output.
"
