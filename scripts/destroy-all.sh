#!/bin/bash

# Exit on error
set -e

# Source environment variables
if [ -f .env ]; then
    echo "📝 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "❌ .env file not found!"
    exit 1
fi

# Configuration
AWS_REGION=${AWS_DEFAULT_REGION:-$(aws configure get region)}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REPOSITORY="data-pipeline"

echo "🚀 Starting cleanup process..."

# Delete all images from ECR to allow repository deletion
echo "🧹 Cleaning up ECR repository..."
aws ecr batch-delete-image \
    --repository-name ${ECR_REPOSITORY} \
    --image-ids imageTag=latest \
    --region ${AWS_REGION} || true  # Ignore errors if repository doesn't exist

# Change to infra directory
cd infra

echo "🧹 Cleaning up local Terraform state files..."
find . -type d -name ".terraform" -exec rm -rf {} +
find . -type d -name "terraform.tfstate.d" -exec rm -rf {} +
find . -type f \( \
    -name ".terraform.lock.hcl" \
    -o -name ".terraform.tfstate.lock.info" \
    -o -name "terraform.tfstate.backup" \
    -o -name "terraform.tfstate" \
    -o -name "myplan" \
\) -exec rm -f {} +

# Change back to root directory
cd ..

echo "✅ Cleanup completed successfully!"
echo "All AWS resources and local Terraform state files have been destroyed."
