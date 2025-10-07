# AWS Deployment Guide

**Fintech Tracker - Bloomberg Terminal for the Everyman**

This guide covers deploying the application to AWS with a cost-optimized architecture.

---

## Architecture Overview

```
[Route 53]
    |
[CloudFront CDN]
    |
    ├─> [S3 Static Site] (Next.js frontend)
    |
    └─> [API Gateway]
            |
        [Lambda] (FastAPI via Mangum)
            |
        [RDS PostgreSQL]
        [ElastiCache Redis]
```

**Monthly Cost Estimate:**
- Free Tier (first 12 months): ~$0-5/mo
- After Free Tier: ~$15-30/mo

---

## Option 1: Serverless Architecture (Recommended for MVP)

### Components

1. **Frontend**: S3 + CloudFront
2. **Backend**: Lambda + API Gateway
3. **Database**: RDS PostgreSQL (db.t3.micro)
4. **Cache**: ElastiCache Redis (cache.t3.micro)
5. **Scheduled Tasks**: EventBridge + Lambda

### Cost Breakdown

| Service | Free Tier | Post Free Tier |
|---------|-----------|----------------|
| S3 | 5GB free | $0.50/mo |
| CloudFront | 1TB free | $1-5/mo |
| Lambda | 1M requests free | $2-5/mo |
| API Gateway | 1M requests free | $1-3/mo |
| RDS (db.t3.micro) | 750 hrs free | $15-20/mo |
| ElastiCache (cache.t3.micro) | 750 hrs free | $10-15/mo |
| **Total** | **$0-5/mo** | **$25-50/mo** |

---

## Option 2: Container Architecture (More Flexible)

### Components

1. **Frontend**: S3 + CloudFront
2. **Backend**: ECS Fargate
3. **Database**: RDS PostgreSQL
4. **Cache**: ElastiCache Redis
5. **Load Balancer**: ALB

### Cost Breakdown

| Service | Monthly Cost |
|---------|--------------|
| S3 + CloudFront | $1-5 |
| ECS Fargate (0.25 vCPU, 0.5GB) | $10-15 |
| RDS (db.t3.micro) | $15-20 |
| ElastiCache (cache.t3.micro) | $10-15 |
| ALB | $16 |
| **Total** | **$52-71/mo** |

---

## Step-by-Step: Serverless Deployment

### Prerequisites

```bash
# Install AWS CLI
brew install awscli  # macOS
# or: pip install awscli

# Configure AWS credentials
aws configure
```

### 1. Database Setup (RDS PostgreSQL)

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier fintech-tracker-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 15.4 \
  --master-username fintech \
  --master-user-password YOUR_SECURE_PASSWORD \
  --allocated-storage 20 \
  --storage-type gp2 \
  --vpc-security-group-ids sg-xxxxx \
  --db-name fintech_tracker \
  --backup-retention-period 7 \
  --publicly-accessible false
```

**Free Tier:** 750 hours/month of db.t3.micro (first 12 months)

### 2. Cache Setup (ElastiCache Redis)

```bash
# Create ElastiCache Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id fintech-tracker-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1 \
  --security-group-ids sg-xxxxx
```

**Free Tier:** 750 hours/month of cache.t3.micro (first 12 months)

### 3. Backend Deployment (Lambda + API Gateway)

#### Prepare Lambda Package

```bash
cd backend

# Install dependencies with Lambda compatibility
pip install -t package -r requirements.txt

# Add Mangum adapter for Lambda
pip install -t package mangum

# Package application
cd package
zip -r ../lambda_function.zip .
cd ..
zip -g lambda_function.zip -r app/
```

#### Create Lambda Function

Create `backend/lambda_handler.py`:

```python
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

Deploy Lambda:

```bash
aws lambda create-function \
  --function-name fintech-tracker-api \
  --runtime python3.10 \
  --handler lambda_handler.handler \
  --zip-file fileb://lambda_function.zip \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-execution-role \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{
    DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/db,
    REDIS_URL=redis://elasticache-endpoint:6379,
    FINPREP_API_KEY=your_key,
    MARKETAUX_API_KEY=your_key
  }"
```

#### Create API Gateway

```bash
aws apigatewayv2 create-api \
  --name fintech-tracker-api \
  --protocol-type HTTP \
  --target arn:aws:lambda:us-east-1:ACCOUNT_ID:function:fintech-tracker-api
```

### 4. Frontend Deployment (S3 + CloudFront)

#### Build Frontend

```bash
cd frontend

# Build for production
npm run build
npm run export  # Generates static files in 'out/' directory
```

#### Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://fintech-tracker-frontend

# Enable static website hosting
aws s3 website s3://fintech-tracker-frontend \
  --index-document index.html \
  --error-document error.html

# Upload files
aws s3 sync out/ s3://fintech-tracker-frontend --acl public-read
```

#### Create CloudFront Distribution

```bash
aws cloudfront create-distribution \
  --origin-domain-name fintech-tracker-frontend.s3.amazonaws.com \
  --default-root-object index.html
```

### 5. Scheduled Tasks (EventBridge + Lambda)

Create daily data ingestion job:

```bash
# Create EventBridge rule (runs daily at 6 AM UTC)
aws events put-rule \
  --name fintech-daily-ingestion \
  --schedule-expression "cron(0 6 * * ? *)"

# Add Lambda target
aws events put-targets \
  --rule fintech-daily-ingestion \
  --targets "Id"="1","Arn"="arn:aws:lambda:REGION:ACCOUNT:function:data-ingestion-lambda"
```

---

## Step-by-Step: Container Deployment (ECS)

### 1. Create Dockerfile

`backend/Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Build and Push to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name fintech-tracker-backend

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build image
cd backend
docker build -t fintech-tracker-backend .

# Tag and push
docker tag fintech-tracker-backend:latest \
  ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fintech-tracker-backend:latest
docker push ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fintech-tracker-backend:latest
```

### 3. Create ECS Task Definition

```json
{
  "family": "fintech-tracker",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/fintech-tracker-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "DATABASE_URL", "value": "postgresql://..."},
        {"name": "REDIS_URL", "value": "redis://..."}
      ]
    }
  ]
}
```

### 4. Create ECS Service

```bash
aws ecs create-service \
  --cluster fintech-tracker-cluster \
  --service-name fintech-tracker-backend \
  --task-definition fintech-tracker \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}"
```

---

## Environment Variables

Set these in Lambda environment variables or ECS task definition:

```bash
DATABASE_URL=postgresql://fintech:password@rds-endpoint:5432/fintech_tracker
REDIS_URL=redis://elasticache-endpoint:6379
FINPREP_API_KEY=your_key
ALPHAVANTAGE_API_KEY=your_key
MARKETAUX_API_KEY=your_key
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

---

## CI/CD Pipeline (GitHub Actions)

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy Lambda
        run: |
          cd backend
          pip install -t package -r requirements.txt
          cd package && zip -r ../function.zip . && cd ..
          zip -g function.zip -r app/
          aws lambda update-function-code \
            --function-name fintech-tracker-api \
            --zip-file fileb://function.zip

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Build and Deploy
        run: |
          cd frontend
          npm install
          npm run build
          npm run export
          aws s3 sync out/ s3://fintech-tracker-frontend
          aws cloudfront create-invalidation --distribution-id DIST_ID --paths "/*"
```

---

## Monitoring & Logging

### CloudWatch Dashboards

```bash
# View Lambda logs
aws logs tail /aws/lambda/fintech-tracker-api --follow

# View RDS metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=fintech-tracker-db
```

### Cost Monitoring

```bash
# Set up billing alerts
aws budgets create-budget \
  --account-id ACCOUNT_ID \
  --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

---

## Production Checklist

- [ ] Set up VPC with private subnets for RDS/ElastiCache
- [ ] Configure security groups (least privilege)
- [ ] Enable RDS automated backups
- [ ] Set up CloudWatch alarms
- [ ] Configure custom domain (Route 53)
- [ ] Enable HTTPS (ACM certificate)
- [ ] Set up WAF for API protection
- [ ] Configure database connection pooling
- [ ] Set up error tracking (Sentry)
- [ ] Enable CloudWatch Logs retention policies
- [ ] Configure CORS properly
- [ ] Set up staging environment

---

## Cost Optimization Tips

1. **Use RDS Reserved Instances** (40-60% savings) after validating usage
2. **Enable S3 Intelligent Tiering** for old data
3. **Use Lambda SnapStart** for faster cold starts
4. **Configure CloudFront caching** aggressively
5. **Set DynamoDB on-demand** for low traffic
6. **Use Spot Instances** for batch jobs
7. **Monitor with Cost Explorer** weekly

---

## Scaling Strategy

### Phase 1: MVP (0-100 users)
- Single RDS instance (db.t3.micro)
- Lambda with minimal concurrency
- Cost: $0-30/mo

### Phase 2: Growth (100-1000 users)
- RDS (db.t3.small)
- Lambda with reserved concurrency
- CloudFront caching
- Cost: $50-100/mo

### Phase 3: Scale (1000+ users)
- RDS (db.t3.medium) with read replicas
- Lambda with auto-scaling
- ElastiCache for session management
- Cost: $150-300/mo

---

## Support Resources

- AWS Free Tier: https://aws.amazon.com/free/
- AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
- AWS Cost Calculator: https://calculator.aws/
