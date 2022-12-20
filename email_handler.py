import smtplib
import os
from dotenv import load_dotenv
from datetime import datetime
from custom_logger import logger

load_dotenv()


def send_email(body: str):
    sender = os.environ.get("MY_EMAIL")
    receiver = os.environ.get("MY_EMAIL")

    try:
        now = datetime.now()
        dt_str = now.strftime("%d/%m/%Y %H:%M:%S")
        text = f"""Hello,
REPORT OF {dt_str}
""" + body
        message = 'Subject: {}\n\n{}'.format("REPORT", text)
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(sender,os.environ.get("APP_PASSWORD_EMAIL"))
        smtp.sendmail(sender, receiver, message)         
        print("Email Sent")
        smtp.quit()
    except smtplib.SMTPException as e:
        logger.error(e,exc_info=True)
        


# def send_log_file():
#     sender = os.environ.get("MY_EMAIL")
#     receiver = os.environ.get("MY_EMAIL")

#     try:
#         now = datetime.now()
#         dt_str = now.strftime("%d/%m/%Y %H:%M:%S")
#         text = f"""Hello,
# LOG FILE OF {dt_str} PFA below
# """
#         message = 'Subject: {}\n\n{}'.format("LOG FILE", text)
#         smtp = smtplib.SMTP('smtp.gmail.com', 587)
#         smtp.starttls()
#         smtp.login(sender,os.environ.get("APP_PASSWORD_EMAIL"))
#         smtp.sendmail(sender, receiver, message)         
#         print("Email Sent with log file attachment")
#         smtp.quit()
#     except smtplib.SMTPException as e:
#         logger.error(e,exc_info=True)