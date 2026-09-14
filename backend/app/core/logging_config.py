import logging
<<<<<<< Updated upstream
from pathlib import Path

=======
import os
from pathlib import Path

from dotenv import load_dotenv
>>>>>>> Stashed changes
from logging.handlers import (
    RotatingFileHandler,
    TimedRotatingFileHandler,
)


<<<<<<< Updated upstream
=======
# Load values from .env
load_dotenv()


>>>>>>> Stashed changes
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

    # Prevent logs from propagating to the root logger/terminal.
    logger.propagate = False

    # Prevent duplicate handlers when FastAPI reloads.
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

<<<<<<< Updated upstream
    # Size of each log file before rotation.
    # 10240 KB = 10 MB
    max_log_kb = 10240

    # Number of old rotated files to keep.
    backup_count = 5
=======
    # Read log configuration from .env
    #
    # Default values are used if variables are missing.
    max_log_kb = int(os.getenv("LOG_MAX_KB", "10240"))
    backup_count = int(os.getenv("LOG_BACKUP_COUNT", "5"))
>>>>>>> Stashed changes

    for name, level in levels.items():

        # =====================================================
        # METHOD 1: NORMAL FILE HANDLER
        # =====================================================
<<<<<<< Updated upstream
        # Simply writes logs into the file.
        #
        # Problem:
        # File keeps growing because there is no rotation.
        #
        # Example:
        # error.log -> 10 MB -> 100 MB -> 1 GB -> ...
        #
=======
>>>>>>> Stashed changes
        # handler = logging.FileHandler(
        #     LOG_DIR / f"{name}.log"
        # )


        # =====================================================
        # METHOD 2: TIME-BASED ROTATION
        # =====================================================
<<<<<<< Updated upstream
        # Rotates the log file based on TIME.
        #
        # Current example:
        # Rotate every midnight and keep 7 old files.
        #
        # Example:
        # error.log
        # error.log.2026-09-09
        # error.log.2026-09-08
        #
=======
>>>>>>> Stashed changes
        # handler = TimedRotatingFileHandler(
        #     LOG_DIR / f"{name}.log",
        #     when="midnight",
        #     interval=1,
        #     backupCount=7,
        # )


        # =====================================================
<<<<<<< Updated upstream
        # METHOD 3: SIZE-BASED ROTATION  <-- CURRENTLY USING
        # =====================================================
        # Rotates the log file when it reaches a specific size.
        #
        # maxBytes:
        # Maximum size of current log file.
        #
        # backupCount:
        # Number of old rotated files to keep.
        #
        # Example:
        #
        # error.log      -> current file
        # error.log.1    -> previous file
        # error.log.2    -> older file
        # ...
        # error.log.5    -> oldest backup
        #
        # We are currently using THIS method.

=======
        # METHOD 3: SIZE-BASED ROTATION
        # =====================================================
>>>>>>> Stashed changes
        handler = RotatingFileHandler(
            LOG_DIR / f"{name}.log",
            maxBytes=max_log_kb * 1024,
            backupCount=backup_count,
        )

        # Minimum level accepted by this handler.
        handler.setLevel(level)

        # Keep only the exact level in each file.
<<<<<<< Updated upstream
        #
        # INFO     -> info.log
        # WARNING  -> warning.log
        # ERROR    -> error.log
        # CRITICAL -> critical.log
=======
>>>>>>> Stashed changes
        handler.addFilter(
            ExactLevelFilter(level)
        )

        # Apply log output format.
        handler.setFormatter(formatter)

<<<<<<< Updated upstream
        # Attach this handler to the "app" logger.
=======
        # Attach handler to logger.
>>>>>>> Stashed changes
        logger.addHandler(handler)

    return logger