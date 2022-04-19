from flask_mail import Message

from app_settings import app, mail


class MailMessage:
    def __init__(self, recipients: list[str], title: str, template: str, sender=app.config['MAIL_DEFAULT_SENDER']):
        self.recipients = recipients
        self.title = title
        self.template = template
        self.sender = sender

    def send(self, **kwargs):
        send_kwargs = {
            "subject": self.title,
            "recipients": self.recipients,
            "html": self.template,
            "sender": self.sender
        }
        send_kwargs = {key: kwargs.get(key, send_kwargs[key]) for key in send_kwargs.keys()}
        msg = Message(**send_kwargs)
        mail.send(msg)


