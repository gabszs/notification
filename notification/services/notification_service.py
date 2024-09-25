from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from icecream import ic
from pydantic import EmailStr

from notification.core.html import html_template
from notification.core.settings import settings
from notification.schemas.file_schema import QueueMessage


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
        self.connection = None

    async def connect(self):
        if not self.connection:
            self.connection = await SMTP(self.smtp_server, self.port)
            await self.connection.starttls()
            await self.connection.login(self.username, self.password)

    async def is_connection_open(self):
        try:
            await self.connection.noop()
            return True
        except Exception:
            return False

    def get_message(self, client_email: EmailStr, mp3_filename: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = client_email
        message["Subject"] = "Success! Your MP3 Is Ready for Download."
        html_body = self.generate_html(mp3_filename)
        message.attach(MIMEText(html_body, "html"))
        return message

    def generate_html(self, mp3_filename: str) -> str:
        return html_template.format(donwload_svc=settings.donwload_svc, mp3_filename=mp3_filename)

    # na v1, ele manda o nome do arquivo e o endpoint de v1/donwload vai puxar do minio
    # mas nas v2, ele vai retoranr o link de share, vai mandar o v2/downlaod, que vai so redirecionar a request para o servico local do minio
    async def __call__(self, queue_message: bytes) -> None:
        try:
            message = QueueMessage.model_validate_json(queue_message)
            email_message = self.get_message(message.client_email, message.mp3_filename)

            if not self.connection or not await self.is_connection_open():
                await self.connect()
            await self.connection.sendmail(email_message)  # type: ignore
        except Exception as error:
            ic(error)
            return True
        return False

    async def close(self):
        if self.connection:
            await self.connection.quit()
            self.connection = None
