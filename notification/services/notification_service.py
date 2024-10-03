import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from icecream import ic
from pydantic import EmailStr

from notification.core.html import html_template
from notification.core.settings import settings
from notification.schemas.file_schema import QueueMessage

# na v1, ele manda o nome do arquivo e o endpoint de v1/donwload vai puxar do minio
# mas nas v2, ele vai retoranr o link de share, vai mandar o v2/downlaod, que vai so redirecionar a request para o servico local do minio


class Notification:
    def __init__(
        self,
        smtp_server: str = settings.smtp_server,
        port: int = settings.email_port,
        sender_email: str = settings.sender_email,
        username: str = settings.login,
        password: str = settings.email_password,
    ) -> None:
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.username = username
        self.password = password
        self.connection: Optional[smtplib.SMTP] = None

    def connect(self) -> None:
        if not self.connection:
            self.connection = smtplib.SMTP(self.smtp_server, self.port)
            self.connection.starttls()  # Inicia TLS
            self.connection.login(self.username, self.password)

    def is_connection_open(self) -> bool:
        try:
            self.connection.noop()  # type: ignore
            return True
        except Exception:
            return False

    def get_message(self, client_email: EmailStr, donwload_link: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = client_email
        message["Subject"] = "Success! Your MP3 Is Ready for Download."
        html_body = self.generate_html(donwload_link)
        message.attach(MIMEText(html_body, "html"))
        return message

    def generate_html(self, download_link: str) -> str:
        return html_template.format(download_link=download_link)

    def __call__(self, queue_message: bytes) -> bool:
        try:
            message = QueueMessage.model_validate_json(queue_message)

            email_message = self.get_message(message.client_email, message.download_link)
            ic(message.download_link)

            if not self.connection or not self.is_connection_open():
                self.connect()
            self.connection.sendmail(self.sender_email, message.client_email, email_message.as_string())  # type: ignore
            ic("Notification successfuly sent")
        except Exception as error:
            ic(error)
            return True
        return False

    def close(self):
        if self.connection:
            self.connection.quit()
            self.connection = None
