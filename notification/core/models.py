from django.db import models


class User(models.Model):
    """Получатель."""

    first_name = models.CharField('Имя', max_length=155)
    phone = models.CharField('Телефон', max_length=12)
    email = models.CharField('Почта', max_length=155)

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ('-first_name',)

    def __str__(self):
        return self.first_name


class Notification(models.Model):
    """Уведомление."""

    TYPE_CHOICES = (
        ('email', 'почта'),
        ('sms', 'сообщение'),
        ('web', 'веб-уведомление')
    )
    STATUS_CHOICES = (
        ('sent', 'отправлено'),
        ('failed', 'провалено'),
        ('queued', 'в очереди')
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Получатель',
        related_name='notifications'
    )
    type = models.CharField(
        'Тип', choices=TYPE_CHOICES, max_length=15,
    )
    content = models.TextField('Содержание')
    status = models.CharField(
        'Статус', default='queued', choices=STATUS_CHOICES, max_length=10
    )
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)
    date_sent = models.DateTimeField('Дата отправки', blank=True, null=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ('-date_created',)

    def __str__(self):
        return self.content[:50]
