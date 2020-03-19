import logging.config


XSERVER_LOGGER_NAME = "xserver"

# This logging configuration defines two log formats:
#   - xserver: outputs just the message
#   - simple: outputs the message with additional information
#
# and two logging destination:
#   - console: logs to STDOUT
#   - xserver: logs to xserver.log
#
# The root (default) logger will output all messages INFO or higher to console.
# A special logger (`XSERVER_LOGGER_NAME`) is defined to log to xserver.log.
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
            "xserver": {"format": "%(message)s"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "xserver": {
                "class": "logging.FileHandler",
                "formatter": "xserver",
                "filename": "xserver.log",
                "mode": "w",
            },
        },
        "loggers": {XSERVER_LOGGER_NAME: {"level": "INFO", "handlers": ["xserver"]}},
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)
