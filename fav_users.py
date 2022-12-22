from os.path import exists
import json
from custom_logger import logger

class FavUsers:
    def __init__(self) -> None:
        self.file_name = "fav_users.json"
        self.input_hint = "Enter user name: use (,) for multiple user names "

    def create_update_users(self, read_write: int = 0) -> list:
        try:
            if not exists(self.file_name):
                print("---FAV USERS does not exists.Creating---")
                user_names = input(self.input_hint)
                map = {
                    "user_names": user_names.split(",")
                }
                json_object = json.dumps(map, indent=4)
                with open(self.file_name, "w") as outfile:
                    outfile.write(json_object)

                return user_names.split(",")

            elif exists(self.file_name):
                if read_write == 0:
                    print("---FAV USERS exists---")
                    with open(self.file_name, "r") as openfile:
                        json_object = json.load(openfile)

                    return json_object["user_names"]

                elif read_write == 1:
                    user_names = input(self.input_hint)
                    with open(self.file_name, "r") as file:
                        json_object = json.load(file)
                        json_object["user_names"].extend(user_names.split(","))

                    with open(self.file_name, "w") as outfile:

                        json_ser = json.dumps(json_object, indent=4)
                        outfile.write(json_ser)

                    return json_object["user_names"]
        except:
            logger.error("Error in fav users")

    def remove_user(self):
        try:
            user_names_input = input(
                "Remove user names : user (,) to remove multiple user names ")
            with open(self.file_name, "r") as file:
                json_object = json.load(file)
                to_remove_lst = user_names_input.split(",")
                final_lst = list(
                    set(json_object["user_names"]) - set(to_remove_lst))
                json_object["user_names"] = final_lst

            with open(self.file_name, "w") as outfile:

                json_ser = json.dumps(json_object, indent=4)
                outfile.write(json_ser)

            return json_object["user_names"]

        except Exception as e:
           logger.error(e,exc_info=True)


