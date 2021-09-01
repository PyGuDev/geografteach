from .models import ConfirmEmail
import uuid


def send_mail(user):
    """Отправка писма подтверждения"""
    code = uuid.uuid1().hex
    ConfirmEmail.objects.create(
        code=code,
        user=user,
    )
    subject = "Активация аккаунта"
    massega = """
        Для активации аккаунта пройдите по ссылке:
        http://geografteach.ru/api/user/confirm/?key={}
    """.format(code)
    from_email = "gubaev1999@gmail.com"
    user.email_user(subject=subject, message=massega, from_email=from_email)
