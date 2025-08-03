import os
import re
import subprocess
import cv2
from collections import deque
import mediapipe as mp





session = os.environ.get("XDG_SESSION_TYPE", "").lower()
if session != "x11":
    print(f"KhatA: In mohit X11 nist! XDG_SESSION_TYPE: {session}")
    exit()
print("Mohit X11 tashkhis dade shod.")


try:
    subprocess.run(["xdotool", "--version"], check=True, stdout=subprocess.PIPE)
except Exception:
    print("KhatA: xdotool nasb nist. Lotfan nasb konid.")
    exit()
print("xdotool nasb shode va amade ast.")


def get_screen_size():
    try:
        out = subprocess.check_output(["xdpyinfo"], stderr=subprocess.PIPE).decode()
        w, h = map(int, re.search(r"dimensions:\s+(\d+)x(\d+)", out).groups())
        return w, h
    except:
        return 1920, 1080

screen_w, screen_h = get_screen_size()


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("KhatA: camera baz nashod!")
    exit()

smooth = deque(maxlen=5)
click_cooldown = 0
SCROLL_THRESHOLD = 40  

with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0]
            x_norm = lm.landmark[8].x
            y_norm = lm.landmark[8].y
            thumb_norm = lm.landmark[4]

            
            mx = int(x_norm * screen_w)
            my = int(y_norm * screen_h)
            smooth.append((mx, my))
            mx_s = int(sum(x for x, _ in smooth) / len(smooth))
            my_s = int(sum(y for _, y in smooth) / len(smooth))

            subprocess.run(["xdotool", "mousemove", str(mx_s), str(my_s)])

            #
            dx = abs(int(thumb_norm.x * w) - int(x_norm * w))
            dy = abs(int(thumb_norm.y * h) - int(y_norm * h))
            if click_cooldown == 0 and dx < 30 and dy < 30:
                subprocess.run(["xdotool", "click", "1"])
                click_cooldown = 15
            else:
                click_cooldown = max(0, click_cooldown - 1)

            
            
            y_diff = (lm.landmark[12].y - lm.landmark[8].y) * h
            if abs(y_diff) > SCROLL_THRESHOLD:
                btn = "4" if y_diff > 0 else "5"
                subprocess.run(["xdotool", "click", btn])

            mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
        else:
            
            pass

        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

