import cv2
import time
import handTrackingModule as htm
import pyautogui
from FingerMovementFunctions import FingerMovements

def main():
    pyautogui.FAILSAFE = False
    # camera frame resolution
    wCam, hCam = 640, 480
    # capture device
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, wCam)
    cap.set(4, hCam)
    x, y = pyautogui.size()
    pTime = index = swipe = fiveUp = volCtrl = cd = vlstp = length = pos_x = vl1 = 0

    detector = htm.handDetector(min_detectioncon=0.75)
    # Storing the fingertips
    tipIds = [4, 8, 12, 16, 20]
    # cool down (in frames)
    cdTime = 40

    while True:
        success, img = cap.read()
        detector.findHands(img)
        lmList = detector.findPosition(img, draw=True)

        if len(lmList) != 0:
            fingers = []
            # Thumb detection - to use the right hand keep the ">" for left hand use "<"
            if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                # if the finger is up, its value is 1, if not its 0
                fingers.append(1)
            else:
                fingers.append(0)
            # Other fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # Actions
            mov = FingerMovements(img, fingers, lmList, cdTime, cd, x, y)
            if cd == 0:
                # the values in "fingers" correspond to [thumb, index, middle finger, ring finger, pinky]
                # For every frame you keep your fingers in one of the positions below, that's a + 1 to It's variable

                if fingers == [0, 1, 0, 0, 0]:
                    index += 1

                elif fingers == [0, 1, 1, 0, 0]:
                    swipe += 1

                elif fingers == [1, 1, 0, 0, 0]:
                    volCtrl += 1

                elif fingers == [1, 1, 1, 1, 1]:
                    fiveUp += 1

                # Fist is the standard position
                elif fingers == [0, 0, 0, 0, 0]:
                    fiveUp = volCtrl = swipe = 0

                    if index >= 25:
                        # releasing the mouse
                        pyautogui.mouseUp(pyautogui.position())
                        index = 0
                        cd = cdTime

                if index >= 22:
                    # sliding the mouse on the Youtube Music player
                    pos_x = mov.slide(lmList[8][1], index)

                elif swipe == 20:
                    # gets the position of the index finger 
                    pos_x = lmList[8][1]

                elif 200 > swipe >= 30:
                    # if the index moved enough it skips or go back a song depending on the direction
                    if mov.swipe(pos_x, lmList[8][1]):
                        pos_x = lmList[8][1]
                        cd = cdTime
                        swipe = 0

                elif swipe >= 200:
                    print("Failed to understand, please try again")
                    swipe = 0

                elif volCtrl == 15:
                    # in case it's muted
                    pyautogui.press('volumeup')
                    # Just for you to see the volume going up and down
                    pyautogui.moveTo(130, 90)

                elif volCtrl >= 17:
                    length, vl1, cd, vlstp, volCtrl = mov.volCtrl(pos_x, lmList[8][1], vlstp, volCtrl, length, vl1)

                # Pause/Continue
                elif fiveUp == 20:
                    cd, fiveUp = mov.pause()

            else:
                cd -= 1

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (10, 25), cv2.FONT_HERSHEY_PLAIN,
                    1.2, (255, 0, 0), 2)
        cv2.putText(img, f'Cooldown : {int(cd)}', (10, 55), cv2.FONT_HERSHEY_PLAIN,
                    1.2, (255, 0, 0), 2)

        cv2.imshow("GestureCapture", img)
        # press 'q' to end the program
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
