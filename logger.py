import logging

from config import settings


logger = logging.Logger("request_logger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(message)s')
filename = settings.get('settings', 'log_path')
file_handler = logging.FileHandler(filename=filename)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def write_to_log_file(method, url, caller_id, entity_type, entity_method, entity_id):
    """Writes formatted message to predefined log file"""

    logger.info(f"{method}:{url}:{caller_id}:{entity_type}:{entity_method}:{entity_id}")

