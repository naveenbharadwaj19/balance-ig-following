from fileinput import filename
import smtplib
import os
from time import sleep
from dotenv import load_dotenv
from email.message import EmailMessage
from datetime import datetime
from custom_logger import logger

load_dotenv()


def send_email(body: str):
    sender = os.environ.get("BHARA_EMAIL")
    receiver = os.environ.get("BHARA_EMAIL")

    try:
        now = datetime.now()
        dt_str = now.strftime("%d/%m/%Y %H:%M:%S")
        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = "REPORT"
        text = f"""Hello,
REPORT OF {dt_str}
""" + body
        msg.set_content(text)
        if os.path.exists("logger.log"):
            with open("logger.log", "rb") as f:
                file_data = f.read()
                msg.add_attachment(
                    file_data, maintype="application", subtype="txt", filename=f.name)
                logger.info("LOG File attached")

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(sender, os.environ.get("BHARA_2FA_PASSWORD_EMAIL"))
        smtp.send_message(msg)  # send
        print("Email Sent")
        logger.info("Email Sent")
        smtp.quit()

    except smtplib.SMTPException as e:
        logger.error(e, exc_info=True)

    except Exception as e:
        logger.error(e, exc_info=True)
