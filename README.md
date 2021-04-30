# Youtube_Music_Player_Gesture_Controller
This project detects gestures from the fingers and execute simple functions on the Youtube Music player, like: go back a video, pause and skip, you can also adjust the computer volume with it. It was created based on some existing projects for hand tracking. It uses the MediaPipe hands tracking solution and the OpenCV library.

## How it works
Basically, it detects which fingers are up and sets values to an array of 5 elements, where every element represents a finger, when the finger is up,  it’s value is 1, if the finger is down the value is 0, so for every frame the list called ‘fingers’ carries the current value of every finger. If ‘fingers’ fall into one of the created categories, it adds a +1 to the correspondent variable, when the variable reaches a value, it starts to execute the function that is connected to that hand position.

## How to use
If you want to test it, there are a few things you need to know: 

* At first you can only use your right hand, palm turned to the webcam. To use the left hand you wanna go to the GestureController.py file, line 32, and change the “>” to “<” on the thumb detection.
```
# Thumb detection - to use the right hand keep the ">" for left hand use "<"
if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
```

* After using a command you want to go back to the fist position, which doesn’t activate any functions.

* You should click on the video tab before trying any gesture.

After knowing that and installing the project as well as the libraries, you wanna execute the ‘GestureController.py’ file. After that you’ll se a window called "GestureCapture" with your camera open, now you can open up Youtube music and start playing a song. There are a few gestures you can try.

## Functions

> Slide
* Keep your index up for a little bit and you should be able to slide through the video while moving your hand from side to side. 

> Swipe
* After a few seconds with your index and middle finger up you can move your hand to the left to skip the video or to the right to go back one.

> Volume Control
* Keep your index and thumb up and you should be able to set your computer volume, after adjusting it, keep your fingers still and it should stop moving the audio bar.

> Pause/Continue
* For this one, just keep all your fingers up for a second.

## References
This project is based on a few existing projects. The ‘handTrackingModule.py’ was created following [this tutorial](https://youtu.be/NZde8Xt78Iw), I also used part of the code from [this video](https://youtu.be/p5Z_GGRCI5s), and for the volume control I used part of the code from [this other video](https://youtu.be/9iEPzbG-xLE). They’re all from the same channel, so if you’re interested in learning about OpenCV or AI you should definitely [check them out](https://www.youtube.com/c/MurtazasWorkshopRoboticsandAI/).
By the way, the inspiration for this project came from [this](https://youtu.be/-_9WFzgI7ak?t=117).

## Documentation

Here are some documentation links:

* [MediaPipe Hands]( https://google.github.io/mediapipe/solutions/hands)

* [OpenCV]( https://docs.opencv.org/master/)

* [Pycaw]( https://github.com/AndreMiras/pycaw) (For the audio control)

* [Pyautogui]( https://pyautogui.readthedocs.io/en/latest/mouse.html) (For the mouse and keyboard control) 

