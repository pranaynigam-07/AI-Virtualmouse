import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import math
from datetime import datetime

# Init
screen_width, screen_height = pyautogui.size()
frame_width, frame_height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, frame_width)
cap.set(4, frame_height)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.85)
mp_draw = mp.solutions.drawing_utils

# Cursor smoothing
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 6

scroll_delay = 0.5
last_scroll_time = 0
last_screenshot_time = 0

# Click tracking
click_count = 0
first_click_time = 0
double_click_threshold = 0.3

# Drag and Drop
drag_mode = False

def get_landmark_positions(hand_landmarks):
    return {
        i: (int(lm.x * frame_width), int(lm.y * frame_height))
        for i, lm in enumerate(hand_landmarks.landmark)
    }

def is_finger_up(landmarks, tip_id):
    return landmarks[tip_id][1] < landmarks[tip_id - 2][1]

def is_finger_half_bent(landmarks, tip_id):
    tip_y = landmarks[tip_id][1]
    pip_y = landmarks[tip_id - 2][1]
    return abs(tip_y - pip_y) < 25

def fingers_pinch(lm, threshold=30):
    x1, y1 = lm[4]   # Thumb tip
    x2, y2 = lm[8]   # Index tip
    distance = math.hypot(x2 - x1, y2 - y1)
    return distance < threshold

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            lm = get_landmark_positions(handLms)

            thumb_up = is_finger_up(lm, 4)
            index_up = is_finger_up(lm, 8)
            middle_up = is_finger_up(lm, 12)
            ring_up = is_finger_up(lm, 16)
            pinky_up = is_finger_up(lm, 20)

            thumb_half = is_finger_half_bent(lm, 4)
            index_half = is_finger_half_bent(lm, 8)
            middle_half = is_finger_half_bent(lm, 12)
            ring_half = is_finger_half_bent(lm, 16)
            pinky_half = is_finger_half_bent(lm, 20)

            current_time = time.time()

            # DRAG MODE
            if fingers_pinch(lm):
                if not drag_mode:
                    drag_mode = True
                    pyautogui.mouseDown()
                    print("Drag started")
                x = np.interp(lm[8][0], (100, frame_width - 100), (0, screen_width))
                y = np.interp(lm[8][1], (100, frame_height - 100), (0, screen_height))
                clocX = plocX + (x - plocX) / smoothening
                clocY = plocY + (y - plocY) / smoothening
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY
            elif drag_mode:
                drag_mode = False
                pyautogui.mouseUp()
                print("Dropped")

            # MOVE MOUSE (Thumb, Index, Middle up)
            elif thumb_up and index_up and middle_up:
                x = np.interp(lm[8][0], (100, frame_width - 100), (0, screen_width))
                y = np.interp(lm[8][1], (100, frame_height - 100), (0, screen_height))
                clocX = plocX + (x - plocX) / smoothening
                clocY = plocY + (y - plocY) / smoothening
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY
                cv2.circle(img, lm[8], 10, (0, 255, 0), cv2.FILLED)

            # LEFT CLICK / DOUBLE CLICK
            if index_half and middle_up and not middle_half:
                if click_count == 0:
                    click_count = 1
                    first_click_time = current_time
                    pyautogui.click()
                    print("Single Click - Waiting for double click")
                elif click_count == 1 and (current_time - first_click_time <= double_click_threshold):
                    pyautogui.doubleClick()
                    print("Double Click")
                    click_count = 0
                else:
                    click_count = 1
                    first_click_time = current_time
                    pyautogui.click()
                    print("Single Click - Resetting timer")
                time.sleep(0.3)

            # RIGHT CLICK
            if middle_half and index_up and not index_half:
                pyautogui.rightClick()
                print("Right Click")
                time.sleep(0.3)

            # SCREENSHOT
            if thumb_half and index_half and middle_half and ring_half and pinky_half:
                if current_time - last_screenshot_time > 1:
                    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pyautogui.screenshot(filename)
                    print(f"Screenshot taken: {filename}")
                    last_screenshot_time = current_time
                    cv2.putText(img, "Screenshot Taken", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # SCROLL UP
            if index_up and middle_up and ring_up:
                if current_time - last_scroll_time > scroll_delay:
                    pyautogui.scroll(300)
                    print("Scroll Up")
                    last_scroll_time = current_time

            # SCROLL DOWN
            if index_half and middle_half and ring_half:
                if current_time - last_scroll_time > scroll_delay:
                    pyautogui.scroll(-300)
                    print("Scroll Down")
                    last_scroll_time = current_time

    cv2.imshow("Smart Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
