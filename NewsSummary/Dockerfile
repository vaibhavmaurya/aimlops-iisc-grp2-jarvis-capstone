# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy the current directory contents into the container
# COPY . /var/task

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/* ${LAMBDA_TASK_ROOT}

# Set the file to be executed when the docker container starts
CMD ["app.lambda_handler"]

# Call it as below
# curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

# Connect to the github using SSH
# /home/guddi/.ssh/id_ed25519
# https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

# docker run -e AWS_ACCESS_KEY_ID=your_access_key -e AWS_SECRET_ACCESS_KEY=your_secret_key -e AWS_DEFAULT_REGION=your_region your_docker_image

# docker run -d -p 9000:8080 --rm --name stocks_ingest -v ./src:/var/task -e AWS_ACCESS_KEY_ID=AKIAR7FVKROU4BVKSQME -e AWS_SECRET_ACCESS_KEY=HDJA/Y5wTSqZdv8wwLWPtrNM3R1DsSFX5zIj4AjR -e AWS_DEFAULT_REGION=ap-south-1 135671745449.dkr.ecr.ap-south-1.amazonaws.com/aimlops-grp2-jarvis-capstone-news-summary

# Reference: https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html


# aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 135671745449.dkr.ecr.ap-south-1.amazonaws.com

# 135671745449.dkr.ecr.ap-south-1.amazonaws.com/aimlops-grp2-jarvis-capstone-news-summary
