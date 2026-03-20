# JupyterHub with configurable-http-proxy
FROM python:3.14-slim

# Install Node.js for configurable-http-proxy
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install configurable-http-proxy globally
RUN npm install -g configurable-http-proxy

# Install JupyterHub and dependencies
RUN pip install --no-cache-dir \
    jupyterhub \
    jupyterhub-nativeauthenticator \
    jupyter \
    notebook

# Create admin user for LocalProcessSpawner (requires system user)
RUN useradd -m -s /bin/bash admin

# Create directory for JupyterHub data
RUN mkdir -p /srv/jupyterhub

WORKDIR /srv/jupyterhub

# Expose JupyterHub port
EXPOSE 8000

# Run JupyterHub
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
