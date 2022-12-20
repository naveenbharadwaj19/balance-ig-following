
from instagrapi import Client, exceptions
from instagrapi.mixins.challenge import ChallengeChoice
from dotenv import load_dotenv
from os.path import exists
import os
from fav_users import FavUsers
from proxies import proxies_lst
import random
from custom_logger import logger
from solve_challenge import get_code_from_email
import schedule
from email_handler import send_email


load_dotenv()


class InstaGram():
    def __init__(self):
        self.cl = Client()
        self.__manage_session()
        self.id = self.cl.user_id

    def __login(self) -> bool:
        user_name = os.environ.get("USER_NAME")
        password = os.environ.get("PASSWORD")
        return self.cl.login(user_name, password)

    def logout(self) -> bool:
        return self.cl.logout()

    def challenge_code_handler(self, choice):
        if choice == ChallengeChoice.EMAIL:
            return get_code_from_email()
        return False

    def set_proxies(self) -> dict:
        proxy = random.choice(proxies_lst)
        user_name = os.environ.get("PROXY_USER_NAME")
        password = os.environ.get("PROXY_PASSWORD")
        self.cl.set_proxy(f"http://{user_name}:{password}@{proxy}")
        print(self.cl.public.proxies)
        return self.cl.public.proxies

    def __manage_session(self):
        try:
            user_name = os.environ.get("USER_NAME")
            self.cl.challenge_code_handler = self.challenge_code_handler
            if not exists("session.json"):
                print(f"---SESSION NOT STORED.SO LOGGING IN AS {user_name}---")
                self.__login()
                self.cl.dump_settings("session.json")
            elif exists("session.json"):
                print(f"SESSION EXISTS of {user_name}")
                self.cl.load_settings("session.json")
                self.__login()
        except Exception as e:
            logger.error(e, exc_info=True)
            print("--Will logout and try again---")
            try:
                is_logged_out = self.logout()
                if is_logged_out:
                    self.__login()
            except Exception as e:
                logger.error(e, exc_info=True)
                print("---STOPPED--- Further action required---")

    def find_user_id_from_user_name(self, user_name: str):
        return self.cl.user_id_from_username(user_name)

    def get_account_details(self):
        return self.cl.account_info().dict()

    def user_info(self, user_name: str):
        return self.cl.user_info_by_username_gql(user_name).dict()

    def followers(self) -> list:
        followers = self.cl.user_followers(self.id)
        followers_filtered = []
        for user in followers.items():
            id = user[0]
            user_name = user[1].username
            followers_filtered.append({"id": id, "user_name": user_name})
        return followers_filtered

    def following(self) -> list:
        following = self.cl.user_following(self.id)
        following_filtered = []
        for user in following.items():
            id = user[0]
            user_name = user[1].username
            following_filtered.append({"id": id, "user_name": user_name})

        return following_filtered

    def balance(self):
        followers = self.followers()
        following = self.following()
        fav_users = FavUsers()
        fav_users_lst = fav_users.create_update_users()
        unfollowed_users_names = []
        for i in following:
            try:
                if not i in followers:
                    user_name = i["user_name"]
                    if not user_name in fav_users_lst:
                        is_verified = self.user_info(user_name)["is_verified"]
                        if not is_verified:
                            is_unfollowed = self.cl.user_unfollow(i["id"])
                            if is_unfollowed:
                                unfollowed_users_names.append(user_name)
            except Exception as e:
                logger.error(e, exc_info=True)
                continue

        no_of_unfollowed_users = len(unfollowed_users_names)

        print(f"Unfollowed {no_of_unfollowed_users}: {unfollowed_users_names}")

        return f"Unfollowed {no_of_unfollowed_users}: {unfollowed_users_names}"


def call_ig():
    try:
        ig = InstaGram()
        balance = ig.balance()
        send_email(balance)
    except (exceptions.GenericRequestError, exceptions.ClientConnectionError, exceptions.PleaseWaitFewMinutes) as e:
        logger.error(e, exc_info=True)
        ig.set_proxies()
        send_email(balance)
        schedule.CancelJob
    except Exception as e:
        logger.error(e, exc_info=True)
        send_email(f"ERROR : {e}")
        schedule.CancelJob
