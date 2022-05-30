import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename='logs/shconfparser.log', level=logging.DEBUG)
logging.info('Logging Time : {}'.format(datetime.now()))
