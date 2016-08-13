# DFIS settings
DFIS_HOST = '10.16.78.84'
DFIS_PORT = 80
DFIS_GROUP = 'dfis'
DFIS_TYPE = 'pypi'
DFIS_DOWNLOAD = '10.16.78.84'

# REDIS
REDIS_HOST = '10.16.76.197'
REDIS_PORT = 6379

HTTP_HOST = ''
HTTP_PORT = 8080

# WSGI Settings
WSGI_LOG = 'default'

# Flask-Log Settings
LOG_LEVEL = 'debug'
LOG_FILENAME = "logs/error.log"
LOG_BACKUP_COUNT = 10
LOG_MAX_BYTE = 1024 * 1024 * 10
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(message)s'
LOG_ENABLE_CONSOLE = True
