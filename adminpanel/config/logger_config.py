from config.settings import LoggerSettings

logging_conf = LoggerSettings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"custom_formatter": {"format": "%(levelname)-10s %(name)-10s [%(asctime)s] : %(message)s"}},
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "custom_formatter",
        },
    },
    "loggers": {
        "rb_producer": {"handlers": ["console_handler"], "level": logging_conf.level, "propagate": False},
        "rb_consumer": {"handlers": ["console_handler"], "level": logging_conf.level, "propagate": False},
        "app": {"handlers": ["console_handler"], "level": logging_conf.level, "propagate": False},
    },
}
