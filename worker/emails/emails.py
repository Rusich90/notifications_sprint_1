import os
import smtplib
from email.message import EmailMessage

from jinja2 import Environment, FileSystemLoader

from config.settings import SMTPSettings


class Emails:
    def __init__(self):
        self.config = SMTPSettings()
        self.server = self._connect()
        self.template_dir = Environment(loader=FileSystemLoader(f'{os.path.dirname(__file__)}/templates'))
        self.data = None

    def _connect(self):
        if self.config.server == 'mailhog':
            server = smtplib.SMTP(self.config.server, self.config.port)
        else:
            server = smtplib.SMTP_SSL(self.config.server, self.config.port)
            server.login(self.config.user, self.config.password.get_secret_value())
        return server

    def _close_connect(self):
        self.server.close()

    def _get_headers(self,):
        message = EmailMessage()
        message["From"] = self.config.user
        message["To"] = ",".join(self.data['recipients'])
        message["Subject"] = self.data['subject']
        return message

    def _render_template(self):
        template = self.template_dir.get_template(self.data['html_template'])
        output = template.render(**self.data)
        return output

    def send_email(self, data: dict):
        self.data = data
        message = self._get_headers()
        template = self._render_template()
        message.add_alternative(template, subtype='html')
        self.server.sendmail(self.config.user, self.data['recipients'], message.as_string())
