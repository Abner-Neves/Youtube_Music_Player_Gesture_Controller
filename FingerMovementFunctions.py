import cv2
import numpy as np
import pyautogui
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL


class FingerMovements:
    def __init__(self, img, fingers, lmList, cdTime, cd, x, y):
        self.img = img
        self.fingers = fingers
        self.lmList = lmList
        self.cdTime = cdTime
        self.cd = cd
        self.x = x
        self.y = y

        # To get the position of the player depending oh the screen size
        # You might wanna change these values if the mouse is not sliding on the player correctly
        self.px = self.x * 0.984375
        self.py = self.y * 0.8687

    def slide(self, currentPosition, index):
        self.currentPosition = currentPosition
        self.index = index

        cv2.putText(self.img, "Choose the part of the song you want", (10, 440),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.3, (0, 140, 255), 2)
        # To save some fps It's running the instructions every 2 frames
        if self.index % 2 == 0:
            pyautogui.mouseDown((self.px - (currentPosition * (3.2))), self.py)

    def swipe(self, previousPostion, currentPosition):
        self.previousPosition = previousPostion
        self.currentPosition = currentPosition

        cv2.putText(self.img, "Swipe to the left to skip - Swipe to the right to go back..", (10, 440),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.2, (0, 140, 255), 2)

        # If you move the index to the left
        if (currentPosition - previousPostion) > 90:
            pyautogui.press("j")
            print("skipping")
            return True

        # If you move it to the right
        elif (currentPosition - previousPostion) < -90:
            # It taps the key twice so it goes to the previous song
            pyautogui.press('k')
            pyautogui.press('k')
            print("going back")
            return True

    def volCtrl(self, previousPostion, currentPosition, vlstp, volCtrl, length, vl1):
        self.previousPosition = previousPostion
        self.currentPosition = currentPosition
        self.vlstp = vlstp
        self.volCtrl = volCtrl
        self.length = length
        self.vl1 = vl1

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]

        cv2.putText(self.img, "After adjusting the volume keep your fingers still", (10, 440),
                    cv2.FONT_HERSHEY_PLAIN,
                    1.3, (0, 140, 255), 2)

        # If you keep the two fingers still for 25 frames it stops
        if vlstp >= 25:
            self.volCtrl = 0
            self.cd = self.cdTime
            self.vlstp = 0
            pyautogui.moveTo(0, 300)

        else:
            # If the index is too low it might see it as a closed finger
            # so It will also work if it detects just the thumb up
            if self.fingers == [1, 1, 0, 0, 0] or self.fingers == [1, 0, 0, 0, 0]:
                a1, b1 = self.lmList[4][1], self.lmList[4][2]
                a2, b2 = self.lmList[8][1], self.lmList[8][2]
                cx, cy = (a1 + a2) // 2, (b1 + b2) // 2
                cv2.circle(self.img, (a1, b1), 8, (200, 80, 0), cv2.FILLED)
                cv2.circle(self.img, (a2, b2), 8, (200, 80, 0), cv2.FILLED)
                cv2.line(self.img, (a1, b1), (a2, b2), (200, 30, 0), 3)
                cv2.circle(self.img, (cx, cy), 5, (200, 80, 0), cv2.FILLED)

                if self.volCtrl == 20:
                    self.vl1 = self.length

                if (self.volCtrl >= 40):
                    # Checks every 20 frames to see if the two fingers moved more than the limit (9 in this case)
                    # if they didn't it just resets the variable's value (vl1)
                    if self.vl1 + 9 < self.length or self.vl1 - 9 > self.length:
                        self.volCtrl = 19
                        self.vl1 = length
                        self.vlstp = 0

                    else:
                        # If they did, the variable that stops the program at 25 gets a +1
                        self.vlstp += 1

                self.length = math.hypot(a2 - a1, b2 - b1)
                self.vol = np.interp(self.length * 1.2, [5, 85], [minVol + 8, maxVol])
                volume.SetMasterVolumeLevel(self.vol, None)

            else:
                self.volCtrl = 0
                self.cd = self.cdTime

        return self.length, self.vl1, self.cd, self.vlstp, self.volCtrl

    def pause(self):
        pyautogui.press('space')
        return int(self.cdTime/2), 0
