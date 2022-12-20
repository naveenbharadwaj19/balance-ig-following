
from time import sleep
import schedule
from ig import call_ig


schedule.every(3).seconds.do(call_ig)

while True:
    schedule.run_pending()
    sleep(1)
