from apscheduler.schedulers.blocking import BlockingScheduler
import time

def foo():
    print(time.time())

# testing blocking scheduler with screen and wsl closed WORKS
scheduler=BlockingScheduler()
scheduler.add_job(foo, 'cron', second=0)
scheduler.start()