# Arguments
ARG access_key_id
ARG secret_access_key
ARG FUNCTION_DIR="/home/app/"

# Grab a fresh copy of the image
FROM python:3.11 as build-image
ARG access_key_id
ARG secret_access_key
ARG FUNCTION_DIR

# Create function directory & copy handler function
RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}
COPY . ${FUNCTION_DIR}
RUN chmod +x ${FUNCTION_DIR}.github/kubernetes/health-check.sh
# Set working directory to function root directory


# Install software and configuration
RUN apt-get update
RUN apt-get install -y gcc openssh-client unixodbc-dev python3-dev default-libmysqlclient-dev build-essential awscli locales locales-all

ENV LC_ALL es_ES.UTF-8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/"
RUN mkdir -p /app/main/tmp

## Configure AWS credentials for CodeArtifact
RUN aws configure set aws_access_key_id $access_key_id
RUN aws configure set aws_secret_access_key $secret_access_key
RUN aws configure set default.region eu-west-1

# Connect to AWS CodeArtifact
RUN aws codeartifact login --tool pip --repository grupotrebolenergia --domain grupotrebolenergia --domain-owner 031061601856 --region eu-west-1

# Install modules
RUN pip install --upgrade pip && \
    pip install --target=${FUNCTION_DIR} -r requirements.txt


# Grab a fresh copy of the Python image
#FROM python:3.11
FROM build-image
#ARG FUNCTION_DIR
# Set working directory
RUN mkdir -p ${FUNCTION_DIR}
WORKDIR ${FUNCTION_DIR}

# Copy the built dependencies and application code from the build-image
#COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
# Set entry point for the container
ENTRYPOINT ["/usr/local/bin/python", "src/main.py"]