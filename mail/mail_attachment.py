import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from os.path import dirname, join
from mail.utils import get_env_var
from mail.constants import (
    PASSWORD,
    PORT,
    SENDER,
    SERVER,
)

load_dotenv()

NOW = datetime.now()
WEEKDAY = NOW.weekday()


class Mail:

    def __init__(self):
        self.port = get_env_var(PORT)
        self.smtp_server_domain_name = get_env_var(SERVER)
        self.sender_mail = get_env_var(SENDER)
        self.password = get_env_var(PASSWORD)

    def send(self, emails):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)

        for email in emails:
            mail = MIMEMultipart('alternative')
            mail['Subject'] = 'Webappnews newsletter'
            mail['From'] = self.sender_mail
            mail['To'] = email

            text_template = f"""
                    Webappnews

                    Bonjour {email.split('@')[0]},
                    Voici un petit aperçu des sujets de l'actualité de ce {NOW.strftime("%d-%m-%Y")}.
                    Passez une bonne journée et à {'demain' if WEEKDAY != 4 else 'lundi'} pour de nouvelles infos.
                    """
            html_template = f"""
                    <h1>Webappnews</h1>

                    <p>Bonjour {email.split('@')[0]},</p>
                    <p>Voici un petit aperçu des sujets de l'actualité de ce <b>{NOW.strftime("%d-%m-%Y")}<b>.<p>
                    <p>Passez une bonne journée et à {'demain' if WEEKDAY != 4 else 'lundi'} pour de nouvelles infos.<p>
                    """

            html_content = MIMEText(html_template.format(email.split("@")[0]), 'html')
            text_content = MIMEText(text_template.format(email.split("@")[0]), 'plain')

            ## attaching messages to MIMEMultipart
            mail.attach(text_content)
            mail.attach(html_content)

            ## attaching an attachment
            filename = 'wordcloud_ACTU_' + NOW.strftime("%d_%m_%Y") + '.png'
            pictures_dir = join(Path(dirname(__file__)).parent, 'wordcloud_fig')
            file_path = join(pictures_dir, filename)
            mimeBase = MIMEBase("application", "octet-stream")
            with open(file_path, "rb") as file:
                mimeBase.set_payload(file.read())
            encoders.encode_base64(mimeBase)
            mimeBase.add_header("Content-Disposition", f"attachment; filename={Path(file_path).name}")
            mail.attach(mimeBase)

            service.sendmail(self.sender_mail, email, mail.as_string())

        service.quit()
