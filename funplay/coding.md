# **DevOps Coding Standards & Best Practices**

---

## **1. Infrastructure as Code (IaC) Standards**

### **General Principles**
```yaml
# GOOD: Declarative, versioned, documented
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = {
    Name        = "web-server"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}

# BAD: Hardcoded values, no metadata
resource "aws_instance" "web" {
  ami           = "ami-12345678"
  instance_type = "t3.micro"
}
```

### **Terraform Standards**
- **File Structure**: Follow consistent module structure
- **Naming Convention**: `snake_case` for resources, `UPPER_SNAKE_CASE` for variables
- **Version Pinning**: Always pin provider/terraform versions
- **State Management**: Never commit `.tfstate` files
- **Variable Validation**: Validate inputs with constraints

```hcl
# variables.tf
variable "instance_count" {
  description = "Number of EC2 instances"
  type        = number
  default     = 2
  
  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 10
    error_message = "Instance count must be between 1 and 10."
  }
}
```

### **CloudFormation/CDK Standards**
```yaml
# Template Metadata
AWSTemplateFormatVersion: "2010-09-09"
Description: "Web Application Stack - Version 1.0.0"

# Parameters with constraints
Parameters:
  InstanceType:
    Type: String
    Default: t3.micro
    AllowedValues: [t3.micro, t3.small, t3.medium]
    Description: EC2 instance type
```

---

## **2. CI/CD Pipeline Standards**

### **Pipeline as Code Structure**
```yaml
# .gitlab-ci.yml or similar
stages:
  - validate
  - test
  - build
  - deploy

# Always include timeout and resource limits
default:
  timeout: 30 minutes
  interruptible: true
  tags:
    - docker
    - linux

# Environment variables for secrets
variables:
  DOCKER_REGISTRY: "$CI_REGISTRY"
  TF_VERSION: "1.5.0"
  
before_script:
  - export COMMIT_SHA=${CI_COMMIT_SHORT_SHA}
  - echo "Starting pipeline for $CI_COMMIT_REF_NAME"

# Job templates for reusability
.job_template: &default_job
  script:
    - echo "Running job"
  after_script:
    - echo "Cleaning up"
  artifacts:
    when: always
    paths:
      - logs/
    expire_in: 1 week
```

### **Build Specifications (Buildkite, CodeBuild, GitHub Actions)**
```yaml
# buildspec.yml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
      nodejs: 18
    commands:
      - pip install --upgrade pip
      - npm ci --only=production
  
  pre_build:
    commands:
      - echo "Logging in to Amazon ECR..."
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
  
  build:
    commands:
      - echo "Building the Docker image..."
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG
  
  post_build:
    commands:
      - echo "Build completed on `date`"
      - echo "Pushing image to ECR..."
      - docker push $ECR_REGISTRY/$IMAGE_REPO_NAME:$IMAGE_TAG
      
# Always include artifact management
artifacts:
  files:
    - '**/*'
  base-directory: 'dist'
  discard-paths: no
```

---

## **3. Configuration Management Standards**

### **Ansible Playbook Standards**
```yaml
---
- name: Configure web server
  hosts: webservers
  become: yes
  gather_facts: yes
  vars:
    http_port: 80
    max_clients: 200
  
  # Use handlers for service management
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
  
  tasks:
    - name: Ensure nginx is installed
      package:
        name: nginx
        state: latest
      notify: restart nginx
    
    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: yes
    
    # Always add idempotency checks
    - name: Check nginx configuration
      command: nginx -t
      register: nginx_test
      changed_when: false
      failed_when: nginx_test.rc != 0
```

### **Dockerfile Standards**
```dockerfile
# Use specific version, not latest
FROM alpine:3.18.3

# Set maintainer and labels
LABEL maintainer="devops-team@company.com"
LABEL version="1.0"
LABEL description="Application container"

# Set environment variables
ENV NODE_ENV=production \
    PORT=3000

# Set non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Install dependencies
RUN apk add --no-cache nodejs npm && \
    npm install -g pm2

# Copy package files first for better caching
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Change ownership
RUN chown -R nodejs:nodejs /app
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/health || exit 1

# Expose port
EXPOSE 3000

# Use exec form for ENTRYPOINT
ENTRYPOINT ["pm2-runtime", "start", "process.yml"]
```

---

## **4. Scripting & Automation Standards**

### **Shell Script Standards**
```bash
#!/usr/bin/env bash

# ==============================================================================
# Script: deploy.sh
# Description: Deployment script for application
# Author: DevOps Team
# Version: 1.0.0
# ==============================================================================

set -euo pipefail  # Fail on error, undefined variables, pipe failures
IFS=$'\n\t'        # Set Internal Field Separator for safer iteration

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"
readonly LOG_FILE="/var/log/${SCRIPT_NAME}.log"

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m' # No Color

# Configuration
readonly DEPLOY_ENV="${DEPLOY_ENV:-staging}"
readonly TIMEOUT=300
readonly MAX_RETRIES=3

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------

log_info() {
    local message="$1"
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - ${message}" | tee -a "$LOG_FILE"
}

log_error() {
    local message="$1"
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - ${message}" | tee -a "$LOG_FILE" >&2
}

validate_prerequisites() {
    local required_commands=("aws" "kubectl" "jq")
    
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_error "Required command '$cmd' is not installed"
            return 1
        fi
    done
}

deploy_application() {
    local namespace="$1"
    local image_tag="$2"
    
    log_info "Starting deployment to namespace: ${namespace}"
    
    # Implementation here
    kubectl set image "deployment/app" "app=ecr-repo:${image_tag}" -n "$namespace"
    
    if kubectl rollout status "deployment/app" -n "$namespace" --timeout="${TIMEOUT}s"; then
        log_info "Deployment successful"
        return 0
    else
        log_error "Deployment failed"
        return 1
    fi
}

# ------------------------------------------------------------------------------
# Main execution
# ------------------------------------------------------------------------------

main() {
    log_info "Starting ${SCRIPT_NAME}"
    
    # Validate inputs
    if [[ $# -lt 2 ]]; then
        log_error "Usage: ${SCRIPT_NAME} <namespace> <image-tag>"
        exit 1
    fi
    
    local namespace="$1"
    local image_tag="$2"
    
    # Validate prerequisites
    if ! validate_prerequisites; then
        exit 1
    fi
    
    # Execute deployment with retry logic
    for ((i=1; i<=MAX_RETRIES; i++)); do
        log_info "Attempt $i of $MAX_RETRIES"
        
        if deploy_application "$namespace" "$image_tag"; then
            log_info "Deployment completed successfully"
            exit 0
        fi
        
        if [[ $i -lt $MAX_RETRIES ]]; then
            log_info "Retrying in 10 seconds..."
            sleep 10
        fi
    done
    
    log_error "All deployment attempts failed"
    exit 1
}

# Trap signals
trap 'log_error "Script interrupted"; exit 130' INT TERM

# Execute main function
main "$@"
```

### **Python Script Standards for DevOps**
```python
#!/usr/bin/env python3
"""
Deployment Automation Script
Handles application deployment to Kubernetes clusters
"""

import argparse
import logging
import sys
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

import boto3
import yaml
from kubernetes import client, config
from kubernetes.client.rest import ApiException


class DeploymentStatus(Enum):
    """Deployment status enumeration."""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"


@dataclass
class DeploymentConfig:
    """Deployment configuration data class."""
    namespace: str
    image_tag: str
    replicas: int
    environment: str
    timeout_seconds: int = 300


class DeploymentManager:
    """Manages Kubernetes deployments."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize deployment manager.
        
        Args:
            config_path: Path to kubeconfig file
        """
        self.logger = self._setup_logging()
        
        try:
            if config_path:
                config.load_kube_config(config_path)
            else:
                config.load_incluster_config()
            
            self.apps_v1 = client.AppsV1Api()
            self.core_v1 = client.CoreV1Api()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Kubernetes client: {e}")
            raise
    
    @staticmethod
    def _setup_logging() -> logging.Logger:
        """Setup structured logging."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def deploy(
        self,
        deployment_config: DeploymentConfig,
        dry_run: bool = False
    ) -> bool:
        """
        Execute deployment.
        
        Args:
            deployment_config: Deployment configuration
            dry_run: If True, only simulate deployment
            
        Returns:
            bool: True if successful, False otherwise
        """
        self.logger.info(
            f"Starting deployment: namespace={deployment_config.namespace}, "
            f"tag={deployment_config.image_tag}"
        )
        
        if dry_run:
            self.logger.info("Dry run mode - no changes will be made")
            return True
        
        try:
            # Update deployment
            deployment = self._get_deployment(deployment_config.namespace)
            
            if not deployment:
                self.logger.error("Deployment not found")
                return False
            
            # Update container image
            deployment.spec.template.spec.containers[0].image = (
                f"myregistry.com/app:{deployment_config.image_tag}"
            )
            
            # Apply update
            self.apps_v1.patch_namespaced_deployment(
                name="myapp",
                namespace=deployment_config.namespace,
                body=deployment
            )
            
            # Wait for rollout
            success = self._wait_for_rollout(deployment_config)
            
            if success:
                self.logger.info("Deployment completed successfully")
            else:
                self.logger.error("Deployment failed")
            
            return success
            
        except ApiException as e:
            self.logger.error(f"Kubernetes API error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False
    
    def _get_deployment(self, namespace: str):
        """Retrieve deployment object."""
        try:
            return self.apps_v1.read_namespaced_deployment(
                name="myapp",
                namespace=namespace
            )
        except ApiException as e:
            self.logger.error(f"Failed to get deployment: {e}")
            return None
    
    def _wait_for_rollout(self, config: DeploymentConfig) -> bool:
        """Wait for deployment rollout to complete."""
        start_time = time.time()
        
        while time.time() - start_time < config.timeout_seconds:
            try:
                deployment = self._get_deployment(config.namespace)
                
                if not deployment:
                    return False
                
                # Check conditions
                for condition in deployment.status.conditions or []:
                    if condition.type == "Progressing" and condition.status == "True":
                        if condition.reason == "NewReplicaSetAvailable":
                            self.logger.info("Rollout completed successfully")
                            return True
                
                time.sleep(5)
                
            except Exception as e:
                self.logger.error(f"Error waiting for rollout: {e}")
                return False
        
        self.logger.error("Rollout timeout exceeded")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Deploy application to Kubernetes")
    
    parser.add_argument(
        "--namespace",
        required=True,
        help="Kubernetes namespace"
    )
    parser.add_argument(
        "--image-tag",
        required=True,
        help="Docker image tag"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate deployment without making changes"
    )
    parser.add_argument(
        "--config",
        help="Path to kubeconfig file"
    )
    
    args = parser.parse_args()
    
    # Create deployment config
    deployment_config = DeploymentConfig(
        namespace=args.namespace,
        image_tag=args.image_tag,
        replicas=2,
        environment="production",
        timeout_seconds=300
    )
    
    # Execute deployment
    try:
        manager = DeploymentManager(args.config)
        success = manager.deploy(deployment_config, args.dry_run)
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logging.error(f"Deployment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## **5. Security & Compliance Standards**

### **Secrets Management**
```yaml
# NEVER commit secrets to version control
# Use environment variables or secret managers

# GOOD: Use secret references
database:
  host: ${DB_HOST}
  password: ${DB_PASSWORD}

# Use tools for secret scanning
# pre-commit hook example
repos:
  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.16.1
    hooks:
      - id: gitleaks
        args: ['--verbose', '--redact']
```

### **Security Scanning in CI/CD**
```yaml
# In pipeline configuration
security_scan:
  stage: security
  script:
    # SAST - Static Application Security Testing
    - trivy config .
    - bandit -r . -f json -o bandit-report.json
    
    # SCA - Software Composition Analysis
    - trivy fs . --scanners vuln
    
    # Container scanning
    - trivy image $IMAGE_NAME:$IMAGE_TAG
    
    # IaC scanning
    - checkov -d .
    
  artifacts:
    reports:
      sast: gl-sast-report.json
      dependency_scanning: gl-dependency-scanning-report.json
    when: always
```

---

## **6. Monitoring & Observability Standards**

### **Logging Standards**
```python
# Structured logging example
import json
import logging
import sys
from pythonjsonlogger import jsonlogger

def setup_structured_logging():
    """Configure structured JSON logging."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # JSON formatter
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        rename_fields={'levelname': 'severity', 'asctime': 'timestamp'},
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Usage
logger = setup_structured_logging()
logger.info("Deployment started", extra={
    "deployment_id": "deploy-123",
    "environment": "production",
    "service": "api-gateway"
})
```

### **Metrics & Tracing**
```python
from prometheus_client import Counter, Histogram, generate_latest
import time

# Define metrics
DEPLOYMENT_COUNTER = Counter(
    'deployment_total',
    'Total number of deployments',
    ['environment', 'status']
)

DEPLOYMENT_DURATION = Histogram(
    'deployment_duration_seconds',
    'Deployment duration in seconds',
    ['environment']
)

def track_deployment(environment: str, func):
    """Decorator to track deployment metrics."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            DEPLOYMENT_COUNTER.labels(
                environment=environment,
                status='success'
            ).inc()
            return result
        except Exception as e:
            DEPLOYMENT_COUNTER.labels(
                environment=environment,
                status='failure'
            ).inc()
            raise
        finally:
            duration = time.time() - start_time
            DEPLOYMENT_DURATION.labels(environment=environment).observe(duration)
    
    return wrapper
```

---

## **7. Documentation & Readability Standards**

### **README Structure**
```markdown
# Project Name

## Overview
Brief description of the infrastructure/service.

## Architecture
!docs/architecture.png

## Prerequisites
- Terraform >= 1.5.0
- AWS CLI v2
- kubectl >= 1.27

## Environment Variables
```bash
export AWS_PROFILE="production"
export TF_VAR_environment="prod"
```

## Usage
### Deployment
```bash
make deploy ENV=production
```

### Destruction
```bash
make destroy ENV=staging
```

## Monitoring
- Dashboard: https://grafana.example.com
- Logs: https://cloudwatch.amazonaws.com
- Alerts: PagerDuty

## Troubleshooting
Common issues and solutions.

## Contributing
Guidelines for contributors.
```

---

## **8. Git & Version Control Standards**

### **Commit Message Convention**
```
type(scope): description

[optional body]

[optional footer]

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting changes
- refactor: Code restructuring
- test: Test updates
- chore: Maintenance tasks
- ci: CI/CD changes
- perf: Performance improvements
- revert: Revert changes

Examples:
feat(terraform): add VPC module
fix(k8s): resolve deployment timeout issue
docs(readme): update installation instructions
ci(gitlab): add security scanning stage
```

### **Git Workflow**
```bash
# Feature branches
git checkout -b feature/terraform-vpc-module
git commit -m "feat(terraform): add VPC configuration"

# Bug fixes
git checkout -b fix/deployment-timeout
git commit -m "fix(deploy): increase timeout to 300s"

# Rebase before merging
git fetch origin
git rebase origin/main
git push --force-with-lease
```

---

## **Key Principles Summary**

1. **Idempotency**: Scripts should produce the same result on repeated executions
2. **Declarative over Imperative**: Define what, not how
3. **Version Everything**: All infrastructure and configurations versioned
4. **Least Privilege**: Minimum necessary permissions
5. **Immutable Infrastructure**: Replace, don't modify
6. **Observability First**: Everything should be monitorable
7. **Automation Everywhere**: Manual steps are failure points
8. **Documentation as Code**: Keep docs with the code
9. **Security by Design**: Security from the beginning
10. **Fail Fast**: Validate early, fail clearly

---

These standards ensure consistency, maintainability, and reliability across all DevOps code and automation. Adjust based on your organization's specific tools and requirements.