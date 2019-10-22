# import the necessary packages
from collections import deque
from playsound import playsound
import numpy as np
import cv2
import imutils
import time
import os
import pygame
from pygame import mixer

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points (IN BGR NOT RGB)

#greenLower = (29, 86, 6)
#greenUpper = (64, 255, 255)

greenLower = (100, 150, 150)
greenUpper = (120, 255, 255)

##greenUpper = (255, 255, 64)
##greenLower = (138, 69, 37)

(dX, dY) = (0, 0)
direction = ""
oldDirection = ""
stop_playing = False
goalLeft = 0
goalRight = 0
left_scored = False
right_scored = False
pygame.mixer.init()

vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vs.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# allow the camera to warm up
time.sleep(2.0)

def draw_boxes(frame):
    #goal rectangles drawn
    cv2.rectangle(frame, (0, 160), (20,320), (0,0,255), 1)
    cv2.rectangle(frame, (640,160), (620,320), (0,0,255), 1)
    
    #quards lines drawn(rows)
    cv2.line(frame, (0,160), (640,160), (255,0,0), 1)
    cv2.line(frame, (0,320), (640,320), (255,0,0), 1)
    #quards lines drawn(cols)
    cv2.line(frame, (160,0), (160,480), (255,0,0,), 1)
    cv2.line(frame, (320,0), (320,480), (255,0,0,), 1)
    cv2.line(frame, (480,0), (480,480), (255,0,0,), 1)


# keep looping
while True:
    # grab the current frame
    ret, frame = vs.read()
    
    # resize the frame, blur it, and convert it to the HSV color space
    #frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = (0,0)
    radius = 0


    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 20:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
               (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
    dX = center[0]
    dY = center[1]
    ballIn = False
    
    # Ball is in quadrant 1
    if dX>0 and dX<160 and dY>0 and dY<160:
        oldDirection = direction
        direction = "Quadrant_1"
        stop_playing = False
        ballIn = True          
    # Ball is in quadrant 2
    if dX>161 and dX<320 and dY>0 and dY<160:
        oldDirection = direction
        direction = "Quadrant_2"
        stop_playing = False
        ballIn = True    
    # Ball is in quadrant 3
    if dX>321 and dX<480 and dY>0 and dY<160:
        oldDirection = direction
        direction = "Quadrant_3"
        stop_playing = False
        ballIn = True          
    # Ball is in quadrant 4
    if dX>481 and dX<640 and dY>0 and dY<160:
        oldDirection = direction
        direction = "Quadrant_4"
        stop_playing = False
        ballIn = True      
        
    # Ball is in quadrant 5
    if dX>0 and dX<160 and dY>161 and dY<320:
        oldDirection = direction
        direction = "Quadrant_5"
        stop_playing = False
        ballIn = True    
    # Ball is in quadrant 6
    if dX>161 and dX<320 and dY>161 and dY<320:
        oldDirection = direction
        direction = "Quadrant_6"
        stop_playing = False
        ballIn = True    
    # Ball is in quadrant 7
    if dX>321 and dX<480 and dY>161 and dY<320:
        oldDirection = direction
        direction = "Quadrant_7"
        stop_playing = False
        ballIn = True    
    # Ball is in quadrant 8
    if dX>481 and dX<640 and dY>161 and dY<320:
        oldDirection = direction
        direction = "Quadrant_8"
        stop_playing = False
        ballIn = True    
      
    # Ball is in quadrant 9
    if dX>0 and dX<160 and dY>321 and dY<480:
        oldDirection = direction
        direction = "Quadrant_9"
        stop_playing = False
        ballIn = True    
    # Ball is in quadrant 10
    if dX>161 and dX<320 and dY>321 and dY<480:
        oldDirection = direction
        direction = "Quadrant_10"
        stop_playing = False
        ballIn = True    
    # Ball is in quadrant 11
    if dX>321 and dX<480 and dY>321 and dY<480:
        oldDirection = direction
        direction = "Quadrant_11"
        stop_playing = False
        ballIn = True    
    # Ball is in quadrant 12
    if dX>481 and dX<640 and dY>321 and dY<480:
        oldDirection = direction
        direction = "Quadrant_12"
        stop_playing = False
        ballIn = True    
            
    
    # Goal 1 (Left Goal)
    if dX < 10 and dY > 161 and dY < 319:
        #play audio of cheering
        oldDirection = direction
        direction = "   Goal"
        stop_playing = False
        ballIn = True
        right_scored = True
        
    # Goal 2 (Right Goal)
    if dX > 620 and dY > 161 and dY < 319:
        #play audio of cheering
        oldDirection = direction
        direction = "   Goal"
        stop_playing = False
        ballIn = True
        left_scored = True        
  

    # If ball is not in any of the areas, it is out 
    if not ballIn:
        direction = "  OUT"
        
    # Adds the score for the left or right team when a goal is scored 
    if oldDirection == "   Goal" and direction != "   Goal":
        if right_scored:
            goalRight += 1
            right_scored = False
            left_scored = False
            
        if left_scored:
            goalLeft += 1
            right_scored = False
            left_scored = False
    
    cv2.putText(frame, direction, (260, 30), cv2.FONT_HERSHEY_SIMPLEX,0.65, (0, 0, 255), 3)
    cv2.putText(frame, "x: {}, y: {}".format(dX, dY),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)
    cv2.putText(frame, ("Left Score" + " - " + str(goalLeft)), (10,30) ,cv2.FONT_HERSHEY_DUPLEX,
                0.65, (255, 255, 0), 2)
    cv2.putText(frame, ("Right Score" + " - " + str(goalRight)), (460,30) ,cv2.FONT_HERSHEY_DUPLEX,
                0.65, (255, 255, 0), 2)

    #call the draw_boxes function to write grids on screen
    draw_boxes(frame)

    # show the frame to our screen
    cv2.imshow("Blind Soccer", frame)

    if direction != oldDirection and direction != "  OUT" and not stop_playing:
        mixer.music.load(direction.lstrip() + ".mp3")
        mixer.music.play(0)
        stop_playing = True
                    
    # press 'q' to exit the video
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

#release handle
vs.release()

# close all windows
cv2.destroyAllWindows()

