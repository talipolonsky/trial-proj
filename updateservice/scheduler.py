from apscheduler.schedulers.background import BackgroundScheduler
from updateservice import update

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update.get_data,'interval', hours= 10)
    scheduler.start()
