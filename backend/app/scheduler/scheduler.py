from apscheduler.schedulers.background import (
    BackgroundScheduler,
)

from app.scheduler.monitoring_job import (
    run_monitoring,
)


scheduler = BackgroundScheduler()


def start_scheduler():

    if not scheduler.running:

        scheduler.add_job(
            run_monitoring,
            "interval",
            minutes=1,
            id="dataset_monitoring",
            replace_existing=True,
        )

        scheduler.start()

        print(
            "Scheduler Started"
        )


def stop_scheduler():

    if scheduler.running:

        scheduler.shutdown()

        print(
            "Scheduler Stopped"
        )