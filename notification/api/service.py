import logging

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from retry import retry

from .exceptions import NotificationError

logger = logging.getLogger(__name__)


class SendNotification:
    """Отправка уведомлений."""

    @staticmethod
    @retry(tries=3, delay=1, backoff=2)
    def send_email(user, content):
        try:
            send_mail(
                subject='Уведомление',
                message=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=(user.email,),
                fail_silently=False,
            )
            logger.info(f'Email отправлен пользователю {user.email}')
            return True
        except Exception as e:
            logger.error(f'Не удалось отправить email: {e}')
            raise NotificationError(f'Ошибка отправки email для {user.email}')

    @staticmethod
    @retry(tries=3, delay=1, backoff=2)
    def send_sms(user, content):
        try:
            # Логика отпраки смс.
            logger.info(
                f'SMS отправлена пользователю {user.first_name}: {content}'
            )
            return True
        except Exception as e:
            logger.error(f'Не удалось отправить SMS (попытка повтора): {e}')
            raise NotificationError(f'Ошибка отправки sms для {user.email}')

    @staticmethod
    @retry(tries=3, delay=1, backoff=2)
    def send_web(user, content):
        try:
            # Логика отправки веб-уведомления.
            logger.info(
                'Web-уведомление отправлено пользователю '
                f'{user.first_name}: {content}'
            )
            return True
        except Exception as e:
            logger.error(
                f'Не удалось отправить веб-уведомление: {e}'
            )
            raise NotificationError(f'Ошибка отправки web=уведомления для {user.email}')

    @staticmethod
    def send_notification(notification):
        """Отправляет уведомление."""
        success = False

        try:
            if notification.type == 'email':
                success = SendNotification.send_email(
                    notification.user, notification.content
                )
            elif notification.type == 'sms':
                success = SendNotification.send_sms(
                    notification.user, notification.content
                )
            elif notification.type == 'web':
                success = SendNotification.send_web(
                    notification.user, notification.content
                )

            notification.status = 'sent' if success else 'failed'
            notification.date_sent = timezone.now()
            notification.save()
            logger.info(
                f'Уведомление {notification.id} отправлено. '
                f'Статус: {notification.status}')
            return success

        except Exception as e:
            logger.exception(f'Ошибка при отправке уведомления: {e}')
            notification.status = 'failed'
            notification.date_sent = timezone.now()
            notification.save()
            return False
