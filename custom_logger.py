# importing module
import logging

# Create and configure logger
logging.basicConfig(filename="logger.log",
					format='%(asctime)s %(message)s',
					)

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.CRITICAL)
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)
