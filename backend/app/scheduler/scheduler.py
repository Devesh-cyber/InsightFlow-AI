from apscheduler.schedulers.background import (
    BackgroundScheduler,
)

from app.scheduler.monitoring_job import (
    run_monitoring
)

scheduler = BackgroundScheduler()


def start_scheduler():
    """
    Start the application scheduler.
    """

    if not scheduler.running:
        scheduler.add_job(
            run_monitoring,
            "interval",
            #hours=1,
            seconds=5,
            id="dataset_monitoring",
            replace_existing=True,
        )
        scheduler.start()
        print('Scheduler Started')


def stop_scheduler():
    """
    Stop the application scheduler.
    """

    if scheduler.running:
        scheduler.shutdown()
        print('Scheduler Stopped')