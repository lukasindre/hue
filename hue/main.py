import random
import concurrent.futures
from enum import Enum
from time import sleep
from .api import Hue
from .config import ENV, GROUPS, ITERS
from .threaded_light_object import ThreadedLightObject

HUE_LIMIT: int = 65535
MAX_BRIGHTNESS: int = 254
MAX_SATURATION: int = 254

def main() -> None:
    """
    main run function
    """
    hue = Hue(ENV["bridge_ip_address"], ENV["username"])
    FUNCTIONS: dict = {
        1: flash_colors(GROUPS["basement"], hue),
        2: flash_random_colors([
            {"light_id": "7", "hue": random.randint},
            {"light_id": "9", "hue": random.randint},
            {"light_id": "11", "hue": random.randint},
            {"light_id": "6", "hue": random.randint},
            {"light_id": "2", "hue": random.randint},
            {"light_id": "10", "hue": random.randint},
            {"light_id": "5", "hue": random.randint},
            {"light_id": "4", "hue": random.randint},
        ]),
        3: around_the_world(["7", "9", "11", "6", "2", "10", "5", "4"], hue)
    }
    while True:
        choice = random.choice(list(FUNCTIONS.items()))
        FUNCTIONS[choice]


def flash_colors(group_id: str, client: Hue) -> None:
    """
    This will flash colors indefinitely
    """
    for _ in enumerate(range(ITERS)):
        hue: int = random.randint(0, HUE_LIMIT)
        client.set_group_state(
            group_id=group_id,
            state={
                "on": True,
                "bri": MAX_BRIGHTNESS,
                "transitiontime": 1,
                "sat": MAX_SATURATION,
                "hue": hue,
            },
        )
        sleep(0.5)
        client.set_group_state(group_id=group_id, state={"bri": 0, "transitiontime": 1})
        sleep(0.5)


def around_the_world(lights: list[str], client: Hue) -> None:
    """
    This will turn on light and turn them off sequentially,
    provided an ordered list of light IDs
    """
    for _ in enumerate(range(ITERS)):
        hue: int = random.randint(0, HUE_LIMIT)
        for light in lights:
            client.set_light_state(
                light_id=light,
                state={
                    "on": True,
                    "bri": MAX_BRIGHTNESS,
                    "transitiontime": 1,
                    "sat": MAX_SATURATION,
                    "hue": hue,
                },
            )
        sleep(0.15)  # give lights a breather
        for light in lights:
            client.set_light_state(
                light_id=light, state={"bri": 0, "transitiontime": 1}
            )


def flash_random_colors(lights: list[ThreadedLightObject], client: Hue) -> None:
    """
    This will turn on a list of lights with different colors
    """
    for _ in enumerate(range(ITERS)):
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_to_light = {
                executor.submit(
                    client.set_light_state,
                    light["light_id"],
                    {
                        "on": True,
                        "bri": MAX_BRIGHTNESS,
                        "sat": MAX_SATURATION,
                        "hue": light["hue"](0, HUE_LIMIT),
                        "transitiontime": 1,
                    },
                ): light
                for light in lights
            }
            for future in concurrent.futures.as_completed(future_to_light):
                light = future_to_light[future]
                try:
                    future.result()
                except Exception as e:
                    print(e)
        sleep(1)
