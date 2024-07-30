import logging.config
from web_app.app import app

log_config = {
    "version": 1,
    "handlers": {
        "stdout": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "level": logging.DEBUG
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "mylog.log",
            "formatter": "default",
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 1,
            "level": logging.INFO
        },
    },
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s: %(module)s - %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S"
        }
    },
    "loggers": {
        "root": {
            "handlers": ["file", "stdout"],
            "level": logging.DEBUG,
            "propagate": True,
        },
    },
}

logging.config.dictConfig(log_config)

__all__ = (
    'app'
)
