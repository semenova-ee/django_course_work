from datetime import datetime

from django.db import models

from members.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.last_name} {self.first_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', **NULLABLE)
    text = models.TextField(verbose_name='текст', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title} {self.text}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class Mailing(models.Model):
    INTERVALS_CHOICES = (
        (1, 'DAILY'),
        (2, 'WEEKLY'),
        (3, 'MONTHLY'),
        (4, 'ONCE')
    )

    STATUS_CHOICES = (
        (1, 'CREATED'),
        (2, 'COMPLETED'),
        (3, 'LAUNCHED'),
        (4, 'FAILED'),
        (5, 'SUSPENDED')
    )

    clients = models.ManyToManyField(Client, verbose_name='Клиенты рассылки')
    start_date = models.DateTimeField(verbose_name='Начало рассылки')
    end_date = models.DateTimeField(verbose_name='Окончание рассылки')
    interval = models.PositiveSmallIntegerField(choices=INTERVALS_CHOICES, null=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, null=True)
    message = models.OneToOneField(Message, on_delete=models.CASCADE,verbose_name='Сообщение', null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    next_try = models.DateTimeField(verbose_name='Попытка следующей отправки', **NULLABLE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.message.title} - {self.start_date} - {self.end_date}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class MailingLog(models.Model):
    time = models.DateTimeField(auto_now=True, verbose_name='Дата и время последней попытки')
    status = models.BooleanField(default=False, verbose_name='Статус последний попытки')
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    schedule = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Расписание', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.schedule.description}: {self.time} - {self.status}'

    class Meta:
        verbose_name = 'Логи рассылки'
        verbose_name_plural = 'Логи рассылок'
        ordering = ('-date_of_last_attempt',)