from pydantic import BaseModel
from fastapi_mail import ConnectionConfig

class MailSettings(BaseModel):
    MAIL_USERNAME: str = "luuquang203@gmail.com"
    MAIL_PASSWORD: str = "gflc rjot cyzr pxkb"
    MAIL_FROM: str = "luuquang203@gmail.com"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

mail_settings = MailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.MAIL_USERNAME,
    MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
    MAIL_FROM=mail_settings.MAIL_FROM,
    MAIL_PORT=mail_settings.MAIL_PORT,
    MAIL_SERVER=mail_settings.MAIL_SERVER,
    MAIL_STARTTLS=mail_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=mail_settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True
)
