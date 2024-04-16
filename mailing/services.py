import datetime

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingLog,  Mailing


def send_mail_now(mailing):
    """
    Функция для отправки почты по заданному расписанию.

    Args:
        schedules: список объектов расписания, по которым нужно отправить почту.
        :param schedule:
    """
    # Получаем сообщение и пользователей для рассылки
    message = mailing.message
    users = Mailing.objects.get(id=mailing.id).clients.all()
    print(users)
    # Отправляем почту каждому пользователю

    try:
        mailing.status = 3
        result = send_mail(
            subject=message.title,
            message=message.text,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email for user in users],
            fail_silently=False,
        )
        # print('sent')
        # print([user.email for user in users])
        # print(result)
        # Если почта отправлена успешно, создаем лог с соответствующим статусом
        MailingLog.objects.create(
            schedule=mailing,
            status_of_last_attempt=True,
            server_response="Сообщение отправлено успешно"
        )

        print("Log created")
        if mailing.end_date and mailing.end_date <= datetime.date.today():
            # Если время рассылки закончилось, обновляем статус расписания на "завершено"
            mailing.status = 2
        mailing.save()

    except Exception as e:
        # Если почта не отправлена, создаем лог с соответствующим статусом и сообщением об ошибке
        MailingLog.objects.create(
            schedule=mailing,
            status_of_last_attempt=False,
            server_response=f"Ошибка при отправке сообщения: {e}"
        )
        print('Schedule failed, check logs')
        mailing.status = 4
        mailing.save()