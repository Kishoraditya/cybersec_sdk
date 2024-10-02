provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "app_server" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 AMI
  instance_type = "t2.micro"

  key_name = var.key_pair_name

  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install docker
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              sudo chkconfig docker on
              sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-\$(uname -s)-\$(uname -m)" -o /usr/local/bin/docker-compose
              sudo chmod +x /usr/local/bin/docker-compose
              mkdir /home/ec2-user/app
              cd /home/ec2-user/app
              git clone https://github.com/kishoraditya/cyberguard-sdk.git .
              echo "NEO4J_URI=${var.neo4j_uri}" >> .env
              echo "NEO4J_USER=${var.neo4j_user}" >> .env
              echo "NEO4J_PASSWORD=${var.neo4j_password}" >> .env
              sudo docker-compose up -d
              EOF

  tags = {
    Name = "CyberGuardAppServer"
  }

  vpc_security_group_ids = [aws_security_group.app_server_sg.id]
}

resource "aws_security_group" "app_server_sg" {
  name        = "app_server_sg"
  description = "Allow SSH and application ports"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.my_ip]
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
