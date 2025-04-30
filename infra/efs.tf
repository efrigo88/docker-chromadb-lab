# EFS File System
resource "aws_efs_file_system" "chromadb" {
  creation_token = "chromadb-storage"
  encrypted      = true

  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }

  tags = {
    Name = "chromadb-storage"
  }
}

# EFS Mount Targets
resource "aws_efs_mount_target" "chromadb" {
  count           = 2
  file_system_id  = aws_efs_file_system.chromadb.id
  subnet_id       = aws_subnet.public[count.index].id
  security_groups = [aws_security_group.efs.id]
}

# EFS Access Point for ChromaDB
resource "aws_efs_access_point" "chromadb" {
  file_system_id = aws_efs_file_system.chromadb.id

  root_directory {
    path = "/chromadb"
    creation_info {
      owner_gid   = 1000
      owner_uid   = 1000
      permissions = "755"
    }
  }

  posix_user {
    gid = 1000
    uid = 1000
  }

  tags = {
    Name = "chromadb-access-point"
  }
}

output "efs_id" {
  value       = aws_efs_file_system.chromadb.id
  description = "ID of the EFS file system for ChromaDB"
}
