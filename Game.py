# !Mediapipe == 0.8.9.1
# !cvzone == 1.5.3
import math
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone
import random
import time

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Find Function
# x is the raw distance y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

coff = np.polyfit(x, y, 2)  # y = Ax^2 + Bx + C

# Game variables
cx, cy = 250, 250
color = (44, 36, 39)
color2 = (142, 138, 138)
color3 = (249, 243, 243)
color4 = (255, 255, 255)
counter = 0
score = 0
timeStart = time.time()
totalTime = 61  # seconds

# Loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 1 -> flips on x-axis

    if time.time() - timeStart < totalTime:

        hands = detector.findHands(img, draw=False)

        if hands:
            lmList = hands[0]["lmList"]
            x, y, w, h = hands[0]["bbox"]
            # print(lmList)

            x1, y1 = lmList[5]
            x2, y2 = lmList[17]

            distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
            A, B, C = coff
            distanceCM = A * distance ** 2 + B * distance + C

            # print(distanceCM, distance)

            if distanceCM < 40:
                if x < cx < x + w and y < cy < y + h:
                    counter = 1

            # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            # cvzone.putTextRect(img, f"{int(distanceCM)} cm", (x + 5, y - 10))

        if counter:
            counter += 1
            color = (255, 255, 255)
            color3 = (44,36, 39)
            color4 = (0, 0, 0)
            if counter == 3:
                cx = random.randint(100, 1100)
                cy = random.randint(100, 600)
                color = (44, 36, 39)
                color3 = (249, 243, 243)
                color4 = (255, 255, 255)
                score += 1
                counter = 0

        # Draw Button
        cv2.circle(img, (cx, cy), 30, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 19, color2, 2)
        cv2.circle(img, (cx, cy), 8, color3, cv2.FILLED)
        cv2.circle(img, (cx, cy), 30, color4, 1)

        # Game HUD
        cvzone.putTextRect(
            img,
            f"Time: {int(totalTime - (time.time() - timeStart))}",
            (1000, 75),
            scale=3,
            offset=20,
        )  # offset is padding
        cvzone.putTextRect(
            img, f"Score: {str(score).zfill(2)}", (60, 75), scale=3, offset=20
        )  # zfill makes it two digit EXAMPLE 01, 02, 03, etc.

    else:
        cvzone.putTextRect(
            img, "Game Over", (400, 240), scale=5, offset=30, thickness=7
        )
        cvzone.putTextRect(img, f"Total Score: {score}", (450, 350), scale=3, offset=20)
        cvzone.putTextRect(img, "Press R to restart", (460, 430), scale=2, offset=10)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord("r"):
        timeStart = time.time()
        score = 0
