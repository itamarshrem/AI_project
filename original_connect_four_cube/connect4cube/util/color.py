def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # If the value is out of range the % 256 value is used.
    # The colours are a transition g - r - b - back to g.
    pos = pos % 256
    if pos < 85:
        r = int(pos*3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return r, g, b
