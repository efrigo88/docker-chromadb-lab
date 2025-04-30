resource "aws_cloudwatch_log_group" "etl_task" {
  name              = "/ecs/etl-task"
  retention_in_days = 30
}
