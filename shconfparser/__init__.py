import logging
from datetime import datetime

logging.basicConfig(filename='logs/shconfparser.log', level=logging.DEBUG)
logging.info('Logging Time : {}'.format(datetime.now()))
