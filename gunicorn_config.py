from os import environ

workers = int(environ.get('GUNICORN_PROCESSES', '3'))
threads = int(environ.get('GUNICORN_THREADS', '1'))

forwarded_allow_ips = '*'
secure_scheme_headers = {'X-Forwarded-Proto': 'https'}
bind = '0.0.0.0:80'
worker_class = 'sync'
