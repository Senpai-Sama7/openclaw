# OpenClaw Cloud Infrastructure — AWS Provisioning Record

## Instance Details
- **Instance ID:** i-0c504a4f15d130993
- **Name:** openclaw-prod
- **Type:** t4g.small (ARM64, 2 vCPU, 2GB RAM, free-tier eligible)
- **AMI:** ami-0f1b9964277dbd54e (Ubuntu 24.04.4 LTS Noble, arm64)
- **Region/AZ:** us-east-1a
- **Public IP:** 18.209.247.78
- **Private IP:** 172.31.10.37
- **Storage:** 30GB gp3, encrypted

## Network
- **VPC:** vpc-081bea0815e07683e (default, 172.31.0.0/16)
- **Subnet:** subnet-07a110c6e3ac903da (us-east-1a)
- **Security Group:** sg-03d96efe67370ce96 (openclaw-sg)
  - Inbound: TCP 22 (SSH), TCP 18789 (OpenClaw gateway) from 0.0.0.0/0
  - Outbound: all traffic (default)

## Access
- **SSH Key:** troy-key (AWS) → ~/.ssh/troy-key-new.pem (local)
- **SSH Command:** `ssh -i ~/.ssh/troy-key-new.pem ubuntu@18.209.247.78`
- **User:** ubuntu (default Ubuntu AMI user)

## AWS Profile
- **Profile:** openclaw
- **Account:** 960451805631
- **IAM User:** troy-automation (Admin group)

## Notes
- Security group allows 0.0.0.0/0 on SSH — Part 2 (hardening) will restrict this
- No Elastic IP assigned — IP will change on stop/start. Consider EIP after hardening.
- Free-tier eligible instance type selected to minimize cost during build phase
