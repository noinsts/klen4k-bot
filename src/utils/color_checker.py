import re

def color_test(color):
    if color.startswith("#"):
        color = color[1:]

    if not re.match(r"^#?[0-9A-Fa-f]{6}$", color):
        return False

    return color
