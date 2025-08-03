import cv2
import mediapipe as mp
import math
import subprocess
import re





mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=2,  
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("no film")
            break

        
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                
                mp_drawing.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                
                h, w, _ = frame.shape
                thumb_tip = handLms.landmark[4]  

                cx, cy = int(thumb_tip.x * w), int(thumb_tip.y * h)

                
                cv2.circle(frame, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

                
                cv2.putText(frame, "Thumb", (cx - 20, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Thumb Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
