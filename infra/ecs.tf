# ECS Configuration
locals {
  # CPU units for the ECS task (1024 units = 1 vCPU)
  task_cpu = 8192 # 8 vCPUs

  # Memory for the ECS task in MiB
  task_memory = 32768 # 32GB

  # Ephemeral storage size in GiB
  ephemeral_storage = 100
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

  ephemeral_storage {
    size_in_gib = local.ephemeral_storage
  }

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
      name      = "chroma"
      image     = "ghcr.io/chroma-core/chroma:1.0.8.dev9"
      essential = true
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      mountPoints = [
        {
          sourceVolume  = "chromadb-storage"
          containerPath = "/chroma/.chroma/index"
          readOnly      = false
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/etl-task"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs-chroma"
        }
      }
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:8000/api/v1/heartbeat || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    },
    {
      name      = "ollama"
      image     = "ollama/ollama:latest"
      essential = true
      portMappings = [
        {
          containerPort = 11434
          hostPort      = 11434
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = "/ecs/etl-task"
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs-ollama"
        }
      }
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:11434/api/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    },
    {
      name      = "etl-container"
      image     = "${aws_ecr_repository.data_pipeline.repository_url}:latest"
      essential = true
      dependsOn = [
        {
          containerName = "ollama"
          condition     = "HEALTHY"
        },
        {
          containerName = "chroma"
          condition     = "HEALTHY"
        }
      ]
      environment = [
        {
          name  = "AWS_REGION"
          value = var.aws_region
        },
        {
          name  = "CHROMA_DB_DIR"
          value = "/chromadb"
        },
        {
          name  = "OLLAMA_HOST"
          value = "http://localhost:11434"
        },
        {
          name  = "THREADS"
          value = "8"
        },
        {
          name  = "DRIVER_MEMORY"
          value = "16g"
        },
        {
          name  = "SHUFFLE_PARTITIONS"
          value = "8"
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
          "awslogs-stream-prefix" = "ecs-etl"
        }
      }
      entryPoint = ["/bin/sh", "-c"]
      command = [
        "curl -X POST http://localhost:11434/api/pull -d '{\"name\":\"nomic-embed-text\"}' && python -m src.main"
      ]
    }
  ])
}

# Output the task definition ARN for easy reference
output "task_definition_arn" {
  value       = aws_ecs_task_definition.etl_task.arn
  description = "ARN of the ECS task definition"
}
