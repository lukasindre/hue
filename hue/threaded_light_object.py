from typing import TypedDict, NotRequired
import random


class ThreadedLightObject(TypedDict):
    """
    This is for multi-threaded light effects
    """

    light_id: str
    hue: random.randint
