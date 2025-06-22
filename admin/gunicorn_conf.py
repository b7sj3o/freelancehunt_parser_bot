from admin.config import settings

reload = settings.DEBUG

# The address and port your Flask app will listen on
bind = f"{settings.ADMIN_HOST}:{settings.ADMIN_PORT}"

# Number of workers. Gunicorn recommends 2-4 workers per core
workers = 1

# The location of your Flask app
wsgi_app = "admin.app:app"

# Set logging - this example logs to a file
accesslog = "-"
errorlog = "-"
