import requests
from typing import Union
from urllib3.exceptions import InsecureRequestWarning
from .state_object import StateObject

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Hue:
    """
    API client for Hue lights
    """

    def __init__(self, ip_address: str, username: str = ""):
        self.ip_address: str = ip_address
        self.username: str = username

    def set_light_state(
        self, light_id: str, state: StateObject
    ) -> requests.models.Response:
        """
        pass in light ID and state object to set
        """
        return self.hue_put(path=f"/lights/{light_id}/state", json=state)

    def set_group_state(
        self, group_id: str, state: StateObject
    ) -> requests.models.Response:
        """
        pass in group ID and state object to set group to
        """
        return self.hue_put(path=f"/groups/{group_id}/action", json=state)

    def hue_get(
        self, path: str, params: Union[dict, None] = None
    ) -> requests.models.Response:
        """
        Perform get requests to the hue api
        """
        return requests.get(url=self.urlify(path), params=params, verify=False)

    def hue_put(
        self,
        path: str,
        params: Union[dict, None] = None,
        json: Union[StateObject, None] = None,
    ) -> requests.models.Response:
        """
        perform post requests to the hue api
        """
        return requests.put(
            url=self.urlify(path), params=params, json=json, verify=False
        )

    def hue_post(
        self,
        path: str,
        params: Union[dict, None] = None,
        json: Union[dict, None] = None,
    ) -> requests.models.Response:
        """
        perform post requests to the hue api
        """
        return requests.post(
            url=self.urlify(path), params=params, json=json, verify=False
        )

    def urlify(self, path: str) -> str:
        """
        this takes your address and appends a path
        """
        return f"https://{self.ip_address}/api/{self.username}{path}"
