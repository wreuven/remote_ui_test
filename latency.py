#
# install dependencies (assumes > Python 3.7)
#
# python -m pip install pywin32
# python -m pip install numpy
# pip install mss==2.0.22
# python -m pip install Pillow
#

import win32api, win32con
import numpy as np
import time

from mss import mss
from PIL import Image

red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)

screen_width  = win32api.GetSystemMetrics(0)
screen_height = win32api.GetSystemMetrics(1)
mon = {'top': int(screen_height/2), 'left': int(screen_width/2), 'width': 10, 'height': 10}
sct = mss()

def ColorDistance(rgb1,rgb2):
    c1 = np.array([rgb1[0]/255,rgb1[1]/255,rgb1[2]/255])
    c2 = np.array([rgb2[0]/255,rgb2[1]/255,rgb2[2]/255])
    rm = 0.5*(c1[0]+c2[0])
    d = sum((2+rm,4,3-rm)*(c1-c2)**2)**0.5
    return d
    
def wait_for_color(c, color):
    finished = 0
    while not finished:
        if ( c != "" ):
            print ("looking for " + c + " rectangle at center of screen")
        sct.get_pixels(mon)
        img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
        pixels = img.load()
        finished = 1
        for i in range(img.size[0]):    # for every col
            for j in range(img.size[1]):    # for every row
                if ( ColorDistance(pixels[i,j],color) > 0.01):
                    finished = 0
   
def click():
    x = int(screen_width/2)
    y = int(screen_height/2)
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    
def start_timer():
    t0 = int(round(time.time() * 1000))
    return t0

def end_timer(t0):
    t1 = int(round(time.time() * 1000))
    print (t1 - t0)
    
def do_test(color):
    time.sleep(2)
    t = start_timer()
    click()
    wait_for_color("", color)
    end_timer(t)   
 
wait_for_color("red", red)

for i in range(10):
    do_test(blue)
    do_test(red)
    