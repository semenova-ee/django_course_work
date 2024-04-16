import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.management.commands.runapscheduler import Command
from mailing.services import send_mail_now

logger = logging.getLogger(__name__)


def check_schedules():
    com = Command
    com.handle()


class CheckCommand(BaseCommand):
    help = "Runs APScheduler."

    def check(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            check_schedules,
            trigger=CronTrigger(minute=1),
            max_instances=1,
        )
        print('Checking....')

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")