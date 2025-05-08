# Use the official Jenkins LTS image (should work on ARM64)
FROM jenkins/jenkins:lts

# Switch to root to install Docker CLI
USER root

# Install prerequisites
RUN apt-get update -y && \
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        software-properties-common

# Add Docker's official GPG key
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Use ARM64 architecture for Docker repo (remove [arch=amd64])
RUN echo "deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
  https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
  > /etc/apt/sources.list.d/docker.list

# Install Docker CLI
RUN apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Jenkins to Docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Optional Docker data dir
VOLUME /var/lib/docker

# Switch back to Jenkins user
USER jenkins
