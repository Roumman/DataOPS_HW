FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

RUN pip install --no-cache-dir \
    jupyterhub \
    jupyterhub-nativeauthenticator \
    jupyter \
    notebook \
    jupyterlab

RUN useradd -m -s /bin/bash admin

RUN mkdir -p /srv/jupyterhub

WORKDIR /srv/jupyterhub

EXPOSE 8000

CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
