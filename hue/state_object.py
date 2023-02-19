from typing import TypedDict, NotRequired


class StateObject(TypedDict):
    on: NotRequired[bool]
    bri: NotRequired[int]
    hue: NotRequired[int]
    sat: NotRequired[int]
    xy: NotRequired[list[float]]
    ct: NotRequired[int]
    alert: NotRequired[str]
    effect: NotRequired[str]
    transitiontime: NotRequired[int]
    bri_inc: NotRequired[int]
    sat_inc: NotRequired[int]
    hue_inc: NotRequired[int]
    ct_inc: NotRequired[int]
    xy_inc: NotRequired[float]
    scene: NotRequired[str]
