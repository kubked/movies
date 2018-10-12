# migrate db on release
release: cd src && python manage.py migrate
# run server and print all logs to STDOUT
web: gunicorn core.wsgi --log-file=- --pythonpath=src
