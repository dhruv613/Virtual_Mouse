# Second Frame: HandTrackingModule.py

import cv2
import mediapipe as mp
import math

class handDetector:
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=mode, max_num_hands=maxHands,
                                        model_complexity=modelComplexity, min_detection_confidence=detectionCon,
                                        min_tracking_confidence=trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        bbox = None
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            x_coords = [lm[1] for lm in lmList]
            y_coords = [lm[2] for lm in lmList]
            bbox = (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
        return lmList, bbox

    def fingersUp(self):
        fingers = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]
            tips = [4, 8, 12, 16, 20]
            for id in tips:
                if id == 4:
                    fingers.append(1 if myHand.landmark[id].x < myHand.landmark[id-2].x else 0)
                else:
                    fingers.append(1 if myHand.landmark[id].y < myHand.landmark[id-2].y else 0)
        return fingers

    def findDistance(self, p1, p2, img, draw=True):
        if self.results.multi_hand_landmarks:
            x1, y1 = self.results.multi_hand_landmarks[0].landmark[p1].x, self.results.multi_hand_landmarks[0].landmark[p1].y
            x2, y2 = self.results.multi_hand_landmarks[0].landmark[p2].x, self.results.multi_hand_landmarks[0].landmark[p2].y
            h, w, c = img.shape
            x1, y1 = int(x1 * w), int(y1 * h)
            x2, y2 = int(x2 * w), int(y2 * h)
            length = math.hypot(x2 - x1, y2 - y1)
            if draw:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            return length, img, [x1, y1, x2, y2, (x1 + x2) // 2, (y1 + y2) // 2]
        return 0, img, None