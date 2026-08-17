from threading import Lock
from enum import Enum
from pathlib import Path

# For flexibility all logs go inside LOG_FOLDER, 
# so if you want to log for a specific guild or process,
# make a file to write to rather than the general one
LOG_FOLDER = Path("logs")
GLOBAL_LOGS = Path("general_logs.txt")

# Must be acquired to write to the log file to avoid data corruption
# To make a file_lock you must acquire lock_maker to avoid race conditions
lock_maker = Lock()
file_locks: dict[str, Lock] = {}

# Log levels for logs
class Level(Enum):
    TRACE   = 0
    DEBUG   = 1
    INFO    = 2
    WARNING = 3
    ERROR   = 4
    FATAL   = 5

class Logger:
    def __init__(self, log_file = LOG_FOLDER + GLOBAL_LOGS):
        self.log_file = log_file

    