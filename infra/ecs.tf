# ECS Configuration
locals {
  # CPU units for the ECS task (1024 units = 1 vCPU)
  task_cpu = 8192 # 8 vCPUs

  # Memory for the ECS task in MiB
  task_memory = 32768 # 32GB
}

# ECS Cluster
resource "aws_ecs_cluster" "data_pipeline" {
  name = "data-pipeline-cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "etl_task" {
  family                   = "etl-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = local.task_cpu
  memory                   = local.task_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  volume {
    name = "chromadb-storage"
    efs_volume_configuration {
      file_system_id     = aws_efs_file_system.chromadb.id
      root_directory     = "/"
      transit_encryption = "ENABLED"
      authorization_config {
        access_point_id = aws_efs_access_point.chromadb.id
      }
    }
  }

  container_definitions = jsonencode([
    {
      name      = "etl-container"
      image     = "${aws_ecr_repository.data_pipeline.repository_url}:latest"
      essential = true
      environment = [
        {
          name  = "AWS_REGION"
          value = var.aws_region
        },
        {
          name  = "CHROMA_DB_DIR"
          value = "/chromadb"
        }
      ]
      mountPoints = [
        {
          sourceVolume  = "chromadb-storage"
          containerPath = "/chromadb"
          readOnly      = false
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/etl-task"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

# Output the task definition ARN for easy reference
output "task_definition_arn" {
  value       = aws_ecs_task_definition.etl_task.arn
  description = "ARN of the ECS task definition"
}
