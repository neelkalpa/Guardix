from surveillance_realtime import normal_camera
from surveillance_realtime_lowlight import low_light_camera
from surveillance_realtime_heatmap import thermal_camera

from sys import argv

def chooseMode(mode):
    if mode == 1: normal_camera()
    elif mode == 2: low_light_camera()
    elif mode == 3: thermal_camera()
    
    
chooseMode(int(argv[1]))
    
