# importing module
import logging,coloredlogs
import os

# Create and configure logger
logging.basicConfig(filename="logger.log",
					format='%(asctime)s %(message)s',
					)

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


coloredlogs.install(level="DEBUG",logger=logger)



def delete_log_file():
    if os.path.exists("logger.log"):
        print("---Logger exists---")