import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 5  # Increased smoothening for better stability
clickDelay = 0.3  # Delay to prevent double click
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
lastClickTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index Finger
        x2, y2 = lmList[12][1:]  # Middle Finger
        x4, y4 = lmList[20][1:]  # Pinky Finger

    # 3. Check which fingers are up
    fingers = detector.fingersUp()

    if len(fingers) < 5:
        fingers += [0] * (5 - len(fingers))  # Ensure the list has 5 elements

    cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 0, 255), 2)

    # 4. Only Index Finger: Moving Mode
    if fingers[1] == 1 and fingers[2] == 0:
        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

        # Prevent accidental pinky misdetection in taskbar area
        if y1 < hScr - 50:  # Avoid errors near the bottom screen
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

    # 5. Both Index and Middle Fingers are Up: Left Click Mode
    if fingers[1] == 1 and fingers[2] == 1:
        length, img, lineInfo = detector.findDistance(8, 12, img)
        if length < 40:
            currentTime = time.time()
            if currentTime - lastClickTime > clickDelay:
                cv2.circle(img, (lineInfo[2], lineInfo[3]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
                lastClickTime = currentTime

    # 6. Three Fingers Up (Index, Middle, Ring): Right Click Mode
    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
        currentTime = time.time()
        if currentTime - lastClickTime > clickDelay:
            autopy.mouse.click(autopy.mouse.Button.RIGHT)
            cv2.putText(img, "Right Click", (100, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            lastClickTime = currentTime

    # 7. Explicit Pinky Finger Up: Scroll Mode (Prevent False Positives)
    if fingers[4] == 1 and fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0:
        autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, True)
        cv2.putText(img, "Scrolling", (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        time.sleep(0.1)  # Prevent excessive scrolling
    else:
        autopy.mouse.toggle(autopy.mouse.Button.MIDDLE, False)

    # 8. Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    # 9. Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
