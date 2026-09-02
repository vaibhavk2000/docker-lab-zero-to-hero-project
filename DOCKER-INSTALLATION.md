# Docker Installation Guide

## Remove Old Versions (if any)
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc

```

## Set Up Docker's Official Repository

```bash
# Add Docker's official GPG key:
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update

```

## Install Docker

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

```

## Start & Enable on Boot

```bash
sudo systemctl start docker
sudo systemctl enable docker

```

## (Optional but Recommended) Run Docker Without `sudo`

```bash
sudo usermod -aG docker $USER
newgrp docker

```

## Verify Installation

```bash
docker --version
docker compose version

```

```

```
