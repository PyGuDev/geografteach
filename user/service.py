import uuid
from django.conf import settings
from .models import ConfirmEmail, User


class Mail:
    @staticmethod
    def send_mail(user: User):
        """Отправка писма подтверждения"""
        code = uuid.uuid1().hex
        ConfirmEmail.objects.create(
            code=code,
            user=user,
        )
        subject = "Активация аккаунта"
        message = """
            Для активации аккаунта пройдите по ссылке:
            {}/api/user/confirm/?key={}
        """.format(settings.SERVER_URL, code)
        from_email = "gubaev1999@gmail.com"
        user.email_user(subject=subject, message=message, from_email=from_email)
