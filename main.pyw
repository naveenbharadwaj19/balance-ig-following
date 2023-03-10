from email_handler import send_email
from instagrapi.exceptions import LoginRequired
from ig import InstaGram

try:
    ig = InstaGram()
    balance = ig.balance()
    send_email(balance)

except LoginRequired as e:
    balance = ig.balance()
    send_email(balance)
