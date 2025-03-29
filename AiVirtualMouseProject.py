# First Frame: AiVirtualMouseProject.py
import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui

# Initialize variables
wCam, hCam = 1920, 1080  # Width and height of the camera frame
frameR = 100  # Frame Reduction to create a margin for hand detection
smoothening = 5  # Smoothing factor for cursor movement
pTime = 0  # Previous time for FPS calculation
plocX, plocY = 0, 0  # Previous location of the cursor
clocX, clocY = 0, 0  # Current location of the cursor
click_threshold = 40  # Distance threshold for detecting clicks
last_click_time = 0  # Debounce time for clicks
fist_closed = False  # Track if fist gesture is detected

# Capture video from the camera
cap = cv2.VideoCapture(0)
cap.set(3, wCam)  # Set width
cap.set(4, hCam)  # Set height

# Initialize hand detector from the HandTrackingModule
detector = htm.handDetector()
wScr, hScr = pyautogui.size()  # Get screen size
sensitivity = wScr / wCam  # Dynamic sensitivity based on screen size

while True:
    # Read frame from the camera
    success, img = cap.read()
    if not success:
        print("Error: Camera not found!")
        break

    # Detect hands and find positions
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Check if landmarks are detected
    if lmList:
        x1, y1 = lmList[8][1:]  # Index finger tip coordinates
        x2, y2 = lmList[4][1:]  # Thumb tip coordinates
        fingers = detector.fingersUp()  # Get the status of fingers

        # Draw rectangle for frame reduction
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Moving Mode (Only Index Finger Up)
        if fingers[1] == 1 and all(f == 0 for f in fingers[2:]):
            # Interpolate finger position to screen coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr * sensitivity))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr * sensitivity))
            clocX = plocX + (x3 - plocX) / smoothening  # Smooth cursor movement
            clocY = plocY + (y3 - plocY) / smoothening
            clocX = max(1, min(wScr - 1, clocX))  # Keep cursor within screen bounds
            clocY = max(1, min(hScr - 1, clocY))
            pyautogui.moveTo(wScr - clocX, clocY)  # Move the cursor

            cv2.circle(img, (x1, y1), 15, (205, 0, 250), cv2.FILLED)  # Draw circle at finger tip
            plocX, plocY = clocX, clocY  # Update previous location

        # Clicking Mode (Index and Middle Finger Touching)
        length, img, lineInfo = detector.findDistance(8, 12, img)  # Find distance between index and middle finger

        if length < click_threshold and time.time() - last_click_time > 0.3:  # Check if fingers are close enough for clicking
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)  # Draw circle at click position
            pyautogui.click()  # Simulate mouse click
            last_click_time = time.time()  # Update last click time

        # Scrolling Mode: Index and Middle Finger Up
        if fingers[1] == 1 and fingers[2] == 1 and all(f == 0 for f in fingers[3:]):
            # Scroll up or down based on finger position
            pyautogui.scroll(15 if y1 < plocY else -15)
            plocY = y1  # Update last position

        # # Minimize Windows (Fist Gesture)
        # if all(f == 0 for f in fingers):
        #     if not fist_closed:  # Only trigger once
        #         print("Fist detected! Minimizing all windows.")
        #         pyautogui.hotkey('win', 'm')
        #         fist_closed = True  # Set state to prevent multiple triggers
        # else:
        #     fist_closed = False  # Reset when hand is open

    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0  # Calculate FPS
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)  # Display FPS

    # Display image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key press
        break

# Release resources
cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows
