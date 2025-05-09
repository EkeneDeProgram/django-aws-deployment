provider "aws" {
  region     = "us-east-1"
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}

resource "aws_key_pair" "deployer" {
  key_name   = var.KEY_NAME
  public_key = file("C:\\Users\\User\\.ssh\\id_rsa.pub")
}

resource "aws_security_group" "django_sg" {
  name_prefix = "django-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
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


# IAM Role and Instance Profile for CloudWatch Agent
resource "aws_iam_role" "ec2_cloudwatch_role" {
  name = "ec2-cloudwatch-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "cloudwatch_attach" {
  name       = "attach-cloudwatch"
  roles      = [aws_iam_role.ec2_cloudwatch_role.name]
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-cloudwatch-profile"
  role = aws_iam_role.ec2_cloudwatch_role.name
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "django_log_group" {
  name = "/aws/ec2/django-app"
}


resource "aws_instance" "django_server" {
  ami                    = "ami-0c02fb55956c7d316"
  instance_type          = "t2.micro"
  key_name               = var.KEY_NAME
  security_groups        = [aws_security_group.django_sg.name]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name

  tags = {
    Name = "DjangoServer"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y python3 git postgresql
              pip3 install --upgrade pip
              amazon-linux-extras enable nginx1
              yum install -y nginx
              systemctl start nginx
              systemctl enable nginx

              # Install CloudWatch Agent
              yum install -y amazon-cloudwatch-agent

              # Create CloudWatch config file
              cat <<EOT > /opt/aws/amazon-cloudwatch-agent/bin/config.json
              {
                "logs": {
                  "logs_collected": {
                    "files": {
                      "collect_list": [
                        {
                          "file_path": "/var/log/messages",
                          "log_group_name": "/aws/ec2/django-app",
                          "log_stream_name": "{instance_id}/messages"
                        },
                        {
                          "file_path": "/var/log/nginx/access.log",
                          "log_group_name": "/aws/ec2/django-app",
                          "log_stream_name": "{instance_id}/nginx-access"
                        }
                      ]
                    }
                  }
                }
              }
              EOT

              # Start CloudWatch Agent
              /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \\
                -a fetch-config \\
                -m ec2 \\
                -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json \\
                -s
              EOF
}
