from threading import Lock
from enum import Enum
from pathlib import Path
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

# For flexibility all logs go inside LOG_FOLDER, 
# so if you want to log for a specific guild or process,
# make a file to write to rather than the general one
LOG_FOLDER = Path("logs")
GLOBAL_LOGS = Path("general_logs.txt")
LOG_FOLDER.mkdir(parents=True, exist_ok=True)

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

# Colour reset
RESET = "\033[0m"
ANSI_CODES = {
    Level.TRACE:   "\033[90m",   # grey
    Level.DEBUG:   "\033[36m",   # cyan
    Level.INFO:    "\033[32m",   # green
    Level.WARNING: "\033[33m",   # yellow
    Level.ERROR:   "\033[31m",   # red
    Level.FATAL:   "\033[1;31m", # bold red
}

class Logger:
    def __init__(self, log_file_name: str = GLOBAL_LOGS.name):
        self.log_file = Path(LOG_FOLDER / log_file_name)

    def _ansi_color(self, level: Level) -> str:
        return ANSI_CODES.get(level)

    def log(self, level: Level, msg: str) -> None:
        log_entry = f"[{level.name}] {msg}"
        time = datetime.now(ZoneInfo("Australia/Sydney"))

        with lock_maker:
            file_lock = file_locks.setdefault(str(self.log_file), Lock())
            with file_lock:
                with open(self.log_file, "a", encoding="utf-8") as file:
                    file.write(f"{log_entry.rstrip()} : {time.isoformat(sep=" ", timespec="seconds")}\n")

        # Print colored output only to the terminal.
        color = self._ansi_color(level)
        print(f"{color}{log_entry.rstrip()}{RESET} : {time.isoformat(sep=" ", timespec="seconds")}", file=sys.stdout)