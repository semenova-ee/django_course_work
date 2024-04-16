from datetime import datetime

from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активность')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.surname} {self.name} - {self.email}'

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
    time = models.TimeField(verbose_name='Время начала')
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
        return f'{self.schedule.title}: {self.time} - {self.status}'
