
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from instagrapi.exceptions import PleaseWaitFewMinutes,LoginRequired
from dotenv import load_dotenv
from os.path import exists
import os
from fav_users import FavUsers
from proxies import proxies_lst
import random
from custom_logger import logger
from solve_challenge import get_code_from_email


load_dotenv()


class InstaGram():
    def __init__(self):
        self.session_file_name = "session.json"
        self.cl = Client()
        self.__manage_session()
        self.id = self.cl.user_id

    def login(self) -> bool:
        user_name = os.environ.get("USER_NAME")
        password = os.environ.get("PASSWORD")
        logger.info(f"--- LOGGING IN AS {user_name} ---")
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
            if not exists(self.session_file_name):
                print(
                    f"--- SESSION NOT STORED.SO LOGGING IN AS {user_name} ---")
                self.login()
                self.cl.dump_settings(self.session_file_name)
            elif exists(self.session_file_name):
                print(f"--- SESSION EXISTS of {user_name} ---")
                self.cl.load_settings(self.session_file_name)
                self.login()
        except Exception as e:
            logger.error(e, exc_info=True)
            print("--- Will logout and try again ---")
            logger.info("--- Will logout and try again ---")
            try:
                is_logged_out = self.logout()
                if is_logged_out:
                    print("Logged out.Logging in...")
                    logger.info(f"LOGGED OUT.LOGGING IN AS... {user_name}")
                    self.__delete_session()
                    self.login()
                    self.cl.dump_settings(self.session_file_name)
            except Exception as e:
                logger.error(f"STOPPED.... {e}", exc_info=True)
                print("---STOPPED--- Further action required---")

    def __delete_session(self) -> bool:
        if exists(self.session_file_name):
            os.remove(self.session_file_name)
            logger.info("Deleted session")
            return True
        return False
            
    def login_required(self):
        is_session_deleted = self.__delete_session()
        if is_session_deleted:
            self.__manage_session()

    def find_user_id_from_user_name(self, user_name: str):
        return self.cl.user_id_from_username(user_name)

    def get_account_details(self):
        return self.cl.account_info().dict()

    def user_info(self, user_name: str):
        return self.cl.user_info_by_username_v1(user_name).dict()

    def followers(self) -> list:
        followers = self.cl.user_followers_v1(self.id)
        followers_filtered = []
        for user in followers:
            id = user.pk
            user_name = user.username
            followers_filtered.append({"id": id, "user_name": user_name})
        return followers_filtered

    def following(self) -> list:
        following = self.cl.user_following_v1(self.id)
        following_filtered = []
        for user in following:
            id = user.pk
            user_name = user.username
            following_filtered.append({"id": id, "user_name": user_name})

        return following_filtered

    def balance(self) -> str:
        try:
          
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
                            is_verified = self.user_info(
                                user_name)["is_verified"]
                            if not is_verified:
                                is_unfollowed = self.cl.user_unfollow(
                                    i["id"])
                                if is_unfollowed:
                                    unfollowed_users_names.append(
                                        user_name)
                except PleaseWaitFewMinutes as pwe:
                    logger.error(pwe)
                    logger.info(
                        f"Setting proxy and trying again ({user_name}) will be skipped")
                    proxy = self.set_proxies()
                    logger.info(proxy)
                    
                    continue

                except Exception as e:
                    logger.error(
                        f"Error while iterating (will be skipped) {user_name} : {e}")

                    continue

            no_of_unfollowed_users = len(unfollowed_users_names)

            print(
                f"Unfollowed {no_of_unfollowed_users}: {unfollowed_users_names}")

            return f"Unfollowed {no_of_unfollowed_users}: {unfollowed_users_names}"
        
        except LoginRequired as lr:
           logger.error(lr)
           self.__delete_session()
           raise LoginRequired
            
        except Exception as e:
            logger.error(e, exc_info=True)
            return str(e)
