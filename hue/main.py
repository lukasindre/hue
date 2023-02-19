import random
import concurrent.futures
from time import sleep
from .api import Hue
from .config import ENV
from .threaded_light_object import ThreadedLightObject

HUE_LIMIT: int = 65535
MAX_BRIGHTNESS: int = 254
MAX_SATURATION: int = 254


def main() -> None:
    """
    main run function
    """
    hue = Hue(ENV["bridge_ip_address"], ENV["username"])
    CHOICES: list[int] = [
        1,
        2,
        3,
    ]
    while True:
        choice = random.choice(CHOICES)
        if choice == 1:
            print(f"Flash Colors now executing {ENV['iters']} times ...")
            flash_colors(ENV["function_config"]["flash_colors"]["basement"], hue)
        elif choice == 2:
            print(f"Flash Random Colors now executing {ENV['iters']} times ...")
            flash_random_colors(ENV["function_config"]["flash_random_colors"], hue)
        elif choice == 3:
            print(f"Around the World now executing {ENV['iters']} times ...")
            around_the_world(ENV["function_config"]["around_the_world"], hue)
        else:
            print("Choice invalid.")
            break


def flash_colors(group_id: str, client: Hue) -> None:
    """
    This will flash colors indefinitely
    """
    for _ in enumerate(range(ENV["iters"])):
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
    for _ in enumerate(range(ENV["iters"])):
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
    for _ in enumerate(range(ENV["iters"])):
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
