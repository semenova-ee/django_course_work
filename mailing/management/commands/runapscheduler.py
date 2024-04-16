import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing
from mailing.services import send_mail_now

logger = logging.getLogger(__name__)


def send_mail_job(schedule_send):
    send_mail_now(schedule_send)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        for schedule in Mailing.objects.filter(periodic=4, is_active=True, status=1):
            scheduler.add_job(
                send_mail_job,
                trigger=CronTrigger(year=schedule.start_date.year,
                                    month=schedule.start_date.month,
                                    day=schedule.start_date.day,
                                    hour=schedule.time.hour,
                                    minute=schedule.time.minute,
                                    second=schedule.time.second),
                id=f'single_schedule_{schedule.id}',  # Уникальный идентификатор для каждого задания
                max_instances=1,
                args=[schedule],
            )
            print('Single schedule add')

        for schedule in Mailing.objects.filter(periodic=2, is_active=True, status=1 or 3):
            scheduler.add_job(
                send_mail_job,
                trigger=CronTrigger(day='*',
                                    hour=schedule.time.hour,
                                    minute=schedule.time.minute,
                                    second=schedule.time.second),
                id=f'daily_schedule_{schedule.id}',  # Уникальный идентификатор для каждого задания
                max_instances=1,
                args=[schedule],
            )
            print('Daily schedule add')

        for schedule in Mailing.objects.filter(periodic=3, is_active=True, status=1 or 3):
            scheduler.add_job(
                send_mail_job,
                trigger=CronTrigger(week='*',
                                    day_of_week=schedule.day_of_week,
                                    hour=schedule.time.hour,
                                    minute=schedule.time.minute,
                                    second=schedule.time.second),
                id=f'weakly_schedule_{schedule.id}',  # Уникальный идентификатор для каждого задания
                max_instances=1,
                args=[schedule],
            )
            print('Weekly schedule add')

        for schedule in Mailing.objects.filter(periodic=4, is_active=True, status=1 or 3):
            scheduler.add_job(
                send_mail_job,
                trigger=CronTrigger(month='*',
                                    day=schedule.day_of_month,
                                    hour=schedule.time.hour,
                                    minute=schedule.time.minute,
                                    second=schedule.time.second),
                id=f'monthly_schedule_{schedule.id}',  # Уникальный идентификатор для каждого задания
                max_instances=1,
                args=[schedule],
            )
            print('Monthly schedule add')
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
