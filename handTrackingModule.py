import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=1, min_detectioncon= 0.7, min_trackingconf =0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = min_detectioncon
        self.trackCon = min_trackingconf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        ##Converts to rgb
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=False):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    # It just changes the colour of the hand connections
                    cv2.circle(img, (cx, cy), 4, (220, 155, 0), cv2.FILLED)

        return lmList