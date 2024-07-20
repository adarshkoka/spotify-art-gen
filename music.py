import cv2
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import json
import cv2 as cv
import urllib.request
import numpy as np
from processing_py import *
import random
import time

# SCOPE = "user-top-read"
SCOPE = ["user-top-read", "user-read-currently-playing"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope=SCOPE))

def getCoverArt(track):

    art = currentTrack['item']['album']['images'][0]
    # art = currentTrack['item']['album']['images'][1]
    # art = currentTrack['item']['album']['images'][2]

    # 0 - 640x640
    # 1 - 300x300 
    # 2 - 64x64

    imageUrl = art['url']

    req = urllib.request.urlopen(imageUrl)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    art = cv2.imdecode(arr, -1)

    dims = art.shape
    global xdim 
    xdim = dims[0]
    global ydim
    ydim = dims[1]

    # cv.imshow('cover-art', art)
    # if cv.waitKey() & 0xff == 27: quit()
    
    return art

def sequin(art, circleSize):
    height = 1200
    width = 800
    app = App(height, width)
    # app.background(255,255,255)
    app.background(0,0,0)

    x = 0
    y = 0
    while(True):
        randX = random.randint(0, xdim - 1)
        randY = random.randint(0, ydim - 1)

        b,g,r = art[randX][randY]

        app.fill(r,g,b)
        # print(r, g, b)
        app.ellipse(x, y, circleSize, circleSize) # draw a circle: center_x, center_y, size_x, size_y
        app.redraw()

        x += circleSize
        if x >= 1200:
            x = 0
            y += circleSize
        if y >= 800:
            break
    
    app.waitAnswer()
    app.exit()

def pixelArt(art, shapeType, shapeSize):
    height = 640
    width = 640
    app = App(height, width)
    # app.background(255,255,255)
    app.background(0,0,0)

    x = 0
    y = 0
    while(True):

        b,g,r = art[y][x]

        app.fill(r,g,b)
        if shapeType == 0:
            app.rect(x, y, shapeSize, shapeSize)
        else:
            app.ellipse(x, y, shapeSize, shapeSize)

        x += shapeSize
        if x >= width:
            x = 0
            y += shapeSize
            app.redraw()
        if y >= height:
            break
    
    app.waitAnswer()
    app.exit()

def ball(art, ballSize):

    width = 1200
    height = 800

    app = App(width, height)
    # app.background(255,255,255)
    app.background(0,0,0)
    app.noFill()

    ballDir = 0

    x = 1
    y = 1

    startTime = time.time()

    while(True):

        randX = random.randint(0, xdim - 1)
        randY = random.randint(0, ydim - 1)
        randColorChangeTimeDiv = random.randint(1, 10)
        colorChangeTime = 4 / randColorChangeTimeDiv

        elapsed = time.time() - startTime
        if elapsed > colorChangeTime:
            startTime = time.time()
            b,g,r = art[randX][randY]
            app.fill(r,g,b)

        app.background(0,0,0) # remove this for trail effect?

        app.ellipse( (height/2) , y, ballSize, ballSize)
        app.redraw()
        
        if y >= height - (ballSize/2):
            ballDir = 1
            x += ballSize # change this to slope
        if y <= 0 + (ballSize/2):
            ballDir = 0
            x += ballSize # change this to slope

        if ballDir == 0:
            y += 10
        else:
            y -= 10

    app.waitAnswer()
    app.exit()


currentTrack = sp.current_user_playing_track()
art = getCoverArt(currentTrack)

# sequin(art, 8)

# 0 for rectangles, 1+ for circles
pixelArt(art, 1, 6) 

# ball(art, 40)

# color bop animation music beats webpage
# bouncing balls
# ribbons

exit()