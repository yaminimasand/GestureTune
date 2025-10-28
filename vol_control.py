import cv2
import mediapipe as mp
import pyautogui
import math
import time

cap = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
draw = mp.solutions.drawing_utils

last_action_time = 0
cooldown = 0.3

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            draw.draw_landmarks(frame, hand)
            lm = hand.landmark

            x1, y1 = int(lm[4].x * w), int(lm[4].y * h)   # Thumb tip
            x2, y2 = int(lm[8].x * w), int(lm[8].y * h)   # Index tip

            cv2.circle(frame, (x1, y1), 8, (0, 0, 255), 3)
            cv2.circle(frame, (x2, y2), 8, (0, 255, 255), 3)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            dist = math.hypot(x2 - x1, y2 - y1) / 4
            cv2.putText(frame, f"Dist: {int(dist)}", (30, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Use cooldown to prevent rapid volume spam
            if time.time() - last_action_time > cooldown:
                if dist > 50:
                    pyautogui.press('volumeup')
                    last_action_time = time.time()
                elif dist < 30:
                    pyautogui.press('volumedown')
                    last_action_time = time.time()

    cv2.imshow("Hand Gesture Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

'''import cv2
import mediapipe as mp
import pyautogui
x1=y1=x2=y2=0
webcam = cv2.VideoCapture(0)
my_hands=mp.solutions.hands.Hands()
drawing_utils=mp.solutions.drawing_utils
while True:
    _,image = webcam.read()
    image=cv2.flip(image,1)
    frame_height, frame_width, _ = image.shape
    rgb_image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    output=my_hands.process(rgb_image)
    hands=output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image,hand)
            landmarks=hand.landmark
            for id,landmark in enumerate(landmarks):
                x=int(landmark.x * frame_width)
                y=int(landmark.y * frame_height)
                if id ==8:
                    cv2.circle(img=image,center=(x,y),radius=8,color=(0,255,255),thickness=3)
                    x1=x
                    y1=y
                if id ==4:
                    cv2.circle(img=image,center=(x,y), radius=8,color=(0,0,255),thickness=3)
                    x2=x
                    y2=y
        dist=((x2-x1)**2+(y2-y1)**2)**0.5/4
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),5)
        if dist>50:
            pyautogui.press('volumeup')
        else:
            pyautogui.press('volumedown')
    cv2.imshow("Hand Volume Control", image)
    key=cv2.waitKey(10)
    if key == 27:
        break
webcam.release()
cv2.destroyAllWindows()'''