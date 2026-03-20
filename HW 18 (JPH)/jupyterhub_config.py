# JupyterHub configuration
# Uses environment variables for secrets (see .env)
import os

c = get_config()

# Cookie secret from environment
c.JupyterHub.cookie_secret_file = os.environ.get(
    'JUPYTERHUB_COOKIE_SECRET_FILE',
    '/srv/jupyterhub/jupyterhub_cookie_secret'
)

# Proxy auth token for configurable-http-proxy
c.ConfigurableHTTPProxy.auth_token = os.environ.get('CONFIGPROXY_AUTH_TOKEN')

# Database URL (SQLite by default, or PostgreSQL from env)
c.JupyterHub.db_url = os.environ.get(
    'JUPYTERHUB_DB_URL',
    'sqlite:///jupyterhub.sqlite'
)

# Bind to all interfaces
c.JupyterHub.bind_url = 'http://:8000'

# Admin user - can login with DummyAuthenticator (any username, no password)
c.Authenticator.admin_users = {'admin'}
c.JupyterHub.admin_access = True

# DummyAuthenticator: allows any username, no password (for dev/demo)
# Replace with NativeAuthenticator for production
c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
