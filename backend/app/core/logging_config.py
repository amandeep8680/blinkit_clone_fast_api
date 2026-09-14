import logging
import os

from pathlib import Path
from dotenv import load_dotenv

from logging.handlers import (
    RotatingFileHandler,
    TimedRotatingFileHandler,
)


# Load values from .env
load_dotenv()


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


class ExactLevelFilter(logging.Filter):
    """
    Allows only the exact logging level.

    Example:
        ERROR    -> error.log
        CRITICAL -> critical.log
    """

    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


def setup_logging():

    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # Prevent logs from propagating
    # to the root logger/terminal.
    logger.propagate = False

    # Prevent duplicate handlers
    # when FastAPI reloads.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    levels = {
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    # ---------------------------------------
    # Read log configuration from .env
    # ---------------------------------------

    # Default = 10240 KB = 10 MB
    max_log_kb = int(
        os.getenv(
            "LOG_MAX_KB",
            "10240",
        )
    )

    # Number of rotated files to keep
    backup_count = int(
        os.getenv(
            "LOG_BACKUP_COUNT",
            "5",
        )
    )

    for name, level in levels.items():

        # ===================================
        # METHOD 1: NORMAL FILE HANDLER
        # ===================================
        # No rotation.
        #
        # handler = logging.FileHandler(
        #     LOG_DIR / f"{name}.log"
        # )


        # ===================================
        # METHOD 2: TIME-BASED ROTATION
        # ===================================
        # Example:
        # error.log
        # error.log.2026-09-13
        #
        # handler = TimedRotatingFileHandler(
        #     LOG_DIR / f"{name}.log",
        #     when="midnight",
        #     interval=1,
        #     backupCount=7,
        # )


        # ===================================
        # METHOD 3: SIZE-BASED ROTATION
        # CURRENTLY USING
        # ===================================
        #
        # error.log
        # error.log.1
        # error.log.2
        # ...
        #
        handler = RotatingFileHandler(
            LOG_DIR / f"{name}.log",
            maxBytes=max_log_kb * 1024,
            backupCount=backup_count,
        )

        # Minimum level accepted
        handler.setLevel(level)

        # INFO     -> info.log
        # WARNING  -> warning.log
        # ERROR    -> error.log
        # CRITICAL -> critical.log
        handler.addFilter(
            ExactLevelFilter(level)
        )

        handler.setFormatter(
            formatter
        )

        logger.addHandler(
            handler
        )

    return logger