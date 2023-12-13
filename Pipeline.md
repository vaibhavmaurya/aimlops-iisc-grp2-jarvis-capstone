# GitHub Action: Deploy to Stock Lambdas

## Overview
This GitHub Action is designed to automate the process of building and deploying container images for stock data management services. It builds new Docker images for different components of a stock data management system, pushes them to Amazon Elastic Container Registry (ECR), and then updates the AWS Lambda functions with these new images upon a push to the "main" branch.

## Action Description

### Set-up Steps
Before using this workflow, you need to:

1. **Create an ECR Repository:**
   - Use AWS CLI to create a repository for storing container images.
   - Update the `ECR_REPOSITORY` and `AWS_REGION` environment variables in the workflow with your repository's name and region.

2. **Create ECS Resources:**
   - Set up an ECS task definition, cluster, and service.
   - Update the `ECS_SERVICE`, `ECS_CLUSTER`, `ECS_TASK_DEFINITION`, and `CONTAINER_NAME` variables with your configurations.

3. **Store IAM User Access Key:**
   - Keep the access key and secret in GitHub Actions secrets as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

### Workflow Details

#### Triggers
- Activates on a push to the "main" branch.

#### Environment Variables
- Configurable AWS region, ECR repositories, ECR registry, and image tags.
- Lambda function ARNs for stock price, stock news, and stock summary services.

#### Jobs
1. **Deploy Job:**
   - Runs on the latest Ubuntu environment.
   - Consists of several steps:

      - **Checkout:** Checks out the source code.

      - **Configure AWS Credentials:** Sets up AWS credentials using the stored GitHub Actions secrets.

      - **Login to Amazon ECR:** Authenticates to ECR to enable pushing images.

      - **Build, Tag, and Push Images:**
         - Builds Docker images for Data Ingestion, News Data Ingestion, and News Summary services.
         - Pushes these images to the respective ECR repositories.

      - **Update AWS Lambda Functions:**
         - Updates the stock price ingestion, stock news ingestion, and stock news summary Lambda functions with the new image URIs from ECR.

### Notes
- Make sure all environment variables and AWS credentials are correctly configured for successful execution.
- The workflow assumes the Dockerfiles for each service are located in the specified directories (`./DataIngestion`, `./NewsDataIngestion`, `./NewsSummary`).
