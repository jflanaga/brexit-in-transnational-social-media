import logging

# Logging
logger = logging.getLogger(__name__)
logger.setLevel('WARNING')

log_file_handler = logging.FileHandler('logs/warnings.txt', 'w+')
log_file_handler.setLevel(logging.WARNING)

# Creating a custom log format for each line in the log file
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)
