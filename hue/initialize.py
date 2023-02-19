import requests
import re
from .config import ENV
from .api import Hue


def main() -> None:
    """
    this is the run function for initializing a username
    """
    while True:
        device: str = input(
            "Enter your device with the following format `app_name#user_name`: "
        )
        if not re.match(r".*#.*", device):
            print(
                f"You entered a value that did not match the format `app_name#user_name`: {device}.\nPlease try again\n"
            )
        else:
            print(f"Success: {device}")
            break

    print("Initializing Hue client ...")
    hue: Hue = Hue(ENV["bridge_ip_address"])
    try:
        print("Attempting to create api user ...")
        r: requests.models.Response = hue.hue_post(
            path="/api", json={"devicetype": device}
        )
        r.raise_for_status()
        r: dict = r.json()[0]
        if r.get("error"):
            print(f"Something went wrong: {r.get('error')}")
            SystemExit()
        elif r.get("success"):
            print(f"Success!  Your api user is {r.get('success').get('username')}")
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e} \nResponse: {r.content}")
