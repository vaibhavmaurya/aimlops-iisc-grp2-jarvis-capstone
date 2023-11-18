# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy the current directory contents into the container
# COPY . /var/task

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/* ${LAMBDA_TASK_ROOT}

# Set the file to be executed when the docker container starts
CMD ["app.lambda_handler"]

# Call it as below
# curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'

# Connect to the github using SSH
# /home/guddi/.ssh/id_ed25519
# https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

# docker run -e AWS_ACCESS_KEY_ID=your_access_key -e AWS_SECRET_ACCESS_KEY=your_secret_key -e AWS_DEFAULT_REGION=your_region your_docker_image

# docker run -d -p 9000:8080 --rm --name stocks_ingest -v ./src:/var/task stocks
