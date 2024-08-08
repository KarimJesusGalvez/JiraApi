import logging
from os import path
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

# TODO config format and filters...

def create_logger_from_subfolder(full_path: str, base_folder: str = "JiraApi") -> logging.Logger:
    """Produces a str with the structure base_folder.SubFolder.Name and configures a logger with the result"""
    log_name = str(Path(full_path).resolve())
    log_name = log_name.split(base_folder + path.sep)[1]
    log_name = log_name.replace(path.sep, ".").replace(path.sep, ".")
    log_name = log_name.replace(path.sep, ".").replace(".py", "")
    return logging.getLogger(log_name)


# TODO filter urllib and Jira output
