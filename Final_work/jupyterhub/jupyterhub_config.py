import os

c = get_config()

c.JupyterHub.cookie_secret_file = os.environ.get(
    'JUPYTERHUB_COOKIE_SECRET_FILE',
    '/srv/jupyterhub/jupyterhub_cookie_secret'
)

c.ConfigurableHTTPProxy.auth_token = os.environ.get('CONFIGPROXY_AUTH_TOKEN')

c.JupyterHub.db_url = os.environ.get(
    'JUPYTERHUB_DB_URL',
    'sqlite:///jupyterhub.sqlite'
)

c.JupyterHub.bind_url = 'http://:8000'

c.Authenticator.admin_users = {'admin'}
c.JupyterHub.admin_access = True

c.JupyterHub.authenticator_class = 'jupyterhub.auth.DummyAuthenticator'
