import numpy as np
def pixel_to_zone(px:int, py:int, img_w:int, img_h:int):
    zone_x = int(px/img_w*1000)
    zone_y = int(py/img_h*1000)
    return zone_x, zone_y
