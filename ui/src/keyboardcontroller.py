"""
Module for interacting with the sysfs interface
"""

from utils.staticvalues import PROGRAM_NAME

import logging
LOGGER = logging.getLogger(PROGRAM_NAME)

KEYBOARD_BRIGHTNESS_FILE = "/sys/devices/platform/clevo_xsm_wmi/kb_brightness"
KEYBOARD_STATE_FILE = "/sys/devices/platform/clevo_xsm_wmi/kb_state"
KEYBOARD_MODE_FILE = "/sys/devices/platform/clevo_xsm_wmi/kb_mode"
KEYBOARD_COLOR_FILE = "/sys/devices/platform/clevo_xsm_wmi/kb_color"

AVAILABLE_KEYBOARD_MODES = {
    "modes": [
        {
            "name": "random_color",
            "value": "0"
        },
        {
            "name": "custom",
            "value": "1"
        },
        {
            "name": "breathe",
            "value": "2"
        },
        {
            "name": "cycle",
            "value": "3"
        },
        {
            "name": "wave",
            "value": "4"
        },
        {
            "name": "dance",
            "value": "5"
        },
        {
            "name": "tempo",
            "value": "6"
        },
        {
            "name": "flash",
            "value": "7"
        }
    ]
}

AVAILABLE_KEYBOARD_COLORS = {
    "colors": [
        {
            "name": "black",
            "colorhexvalue": "0x000000"
        },
        {
            "name": "red",
            "colorhexvalue": "0xFF0000"
        },
        {
            "name": "green",
            "colorhexvalue": "0x00FF00"
        },
        {
            "name": "yellow",
            "colorhexvalue": "0xFFFF00"
        },
        {
            "name": "blue",
            "colorhexvalue": "0x0000FF"
        },
        {
            "name": "magenta",
            "colorhexvalue": "0xFF00FF"
        },
        {
            "name": "cyan",
            "colorhexvalue": "0x00FFFF"
        },
        {
            "name": "white",
            "colorhexvalue": "0xFFFFFF"
        }
    ]
}

KEYBOARD_DEFAULT_COLOR = "blue"

KEYBOARD_STATE_OFF = 0
KEYBOARD_STATE_ON = 1

KEYBOARD_MIN_BRIGHTNESS = 1
KEYBOARD_MAX_BRIGHTNESS = 10
KEYBOARD_STEP_BRIGHTNESS = 1

def get_keyboard_mode():
    """
    Get the current keyboard backlight mode

    Returns a number between 0 and 7. On a error returns -1
    """
    mode = -1

    try:
        LOGGER.debug("read keyboard mode file")
        with open(KEYBOARD_MODE_FILE, "r") as kb_file:
            mode = kb_file.read().rstrip()
    except IOError as err:
        LOGGER.exception(err)

    return mode

def set_keyboard_mode(mode_name):
    """
    Set the keyboard mode

    Arguments:
        mode_name: The name of the mode. The available modes are in AVAILABLE_KEYBOARD_MODES dictonary
    """

    LOGGER.debug("check if mode_name is empty")
    if mode_name == "":
        LOGGER.error("Mode is empty")
        return

    LOGGER.debug("check if mode_name is available")
    if sum([x["name"] == mode_name for x in AVAILABLE_KEYBOARD_MODES["modes"]]) == 0:
        LOGGER.error("The Mode '%s' is not supported", mode_name)
        return

    mode_value = ""

    LOGGER.debug("get the mode information")
    for mode in AVAILABLE_KEYBOARD_MODES["modes"]:
        if mode["name"] == mode_name:
            LOGGER.debug("finding value: %s", str(mode["value"]))
            mode_value = str(mode["value"])

    LOGGER.debug("mode value: %s", mode_value)

    try:
        LOGGER.debug("write mode into sysfs")
        with open(KEYBOARD_MODE_FILE, "w") as kb_file:
            kb_file.write(mode_value)
    except IOError as err:
        LOGGER.exception(err)

def get_keyboard_state():
    """
    Get the current keyboard backlight state

    Returns a number between 0 and 1. On a error returns -1

    The state 1 is keyboard backlight is on
    The state 0 is keyboard backlight is off
    """

    state = -1

    try:
        LOGGER.debug("read keyboard state file")
        with open(KEYBOARD_STATE_FILE, "r") as kb_file:
            state = kb_file.read().rstrip()
    except IOError as err:
        LOGGER.exception(err)

    return state

def set_keyboard_state(state):
    """
    Set the keyboard state

    Arguments:
        state: The value of state. The available are 0 (Off) and 1 (On)
    """

    LOGGER.debug("check if state is empty")
    if state == "":
        LOGGER.error("The State is empty")
        return

    LOGGER.debug("check if state 0 or 1")
    if state not in ["0", "1"]:
        LOGGER.error("The State '%s' was not supported", state)
        return

    try:
        LOGGER.debug("write state into sysfs")
        with open(KEYBOARD_STATE_FILE, "w") as kb_file:
            kb_file.write(state)
    except IOError as err:
        LOGGER.exception(err)

def get_keyboard_color():
    """
    Get the current keyboard backlight color

    Returns a dict with the keyboard color information of left, mid and right region
    """
    
    try:
        LOGGER.debug("read keyboard color file")
        with open(KEYBOARD_COLOR_FILE, "r") as kb_file:
            color = kb_file.read().rstrip()
    except IOError as err:
        LOGGER.exception(err)
        return ""

    color_list = color.split(" ")

    colors = {}
    
    LOGGER.debug("create keyboard color dictonary")
    if len(color_list) == 1:
        return {
                {
                    "left": color_list[0],
                    "middle": color_list[0],
                    "right": color_list[0]
                }
            }
    else:
        return {
                    "left": color_list[0],
                    "middle": color_list[1],
                    "right": color_list[2]
                }

def set_keyboard_color(colors):
    """
    Set the keyboard color

    Arguments:
        colors: Are dictonary with the colors and regions
    """

    LOGGER.debug("check if dict empty")
    if not bool(colors):
        print("Color is empty")
        return

    color_list = ["", "", ""]
    region_list = {"left":0, "middle":1, "right":2}

    LOGGER.debug("check dictonary colors and convert the dict into list")
    for region, color in colors.items():
        if sum([x["name"] == color for x in AVAILABLE_KEYBOARD_COLORS["colors"]]) == 0:
            LOGGER.error("The Color %s' is not supported", color)
            color = KEYBOARD_DEFAULT_COLOR

        color_list[region_list[region]] = color

    try:
        LOGGER.debug("write keyboard color file")
        with open(KEYBOARD_COLOR_FILE, "w") as kb_file:
            kb_file.write(" ".join(color_list))
    except IOError as err:
        LOGGER.exception(err)

def get_keyboard_brightness():
    """
    Get the current keyboard backlight brightness

    Returns a number between 1 and 10. On a error returns -1
    """

    brightness = -1

    try:
        LOGGER.debug("read keyboard brightness file")
        with open(KEYBOARD_BRIGHTNESS_FILE, "r") as kb_file:
            brightness = kb_file.read().rstrip()
    except IOError as err:
        LOGGER.exception(err)

    return brightness

def set_keyboard_brightness(brightness):
    """
    Set the keyboard brightness

    Arguments:
        brightness: A value between 1 and 10
    """

    LOGGER.debug("check if brightness empty")
    if brightness == "":
        print("Brightness is empty")
        return

    LOGGER.debug("check if the value is in range")
    if int(brightness) < KEYBOARD_MIN_BRIGHTNESS or int(brightness) > KEYBOARD_MAX_BRIGHTNESS:
        LOGGER.error("The Brightness Value '%s' was not supported")
        return

    try:
        LOGGER.debug("write keyboard brightness file")
        with open(KEYBOARD_BRIGHTNESS_FILE, "w") as kb_file:
            kb_file.write(brightness)
    except IOError as err:
        LOGGER.exception(err)
