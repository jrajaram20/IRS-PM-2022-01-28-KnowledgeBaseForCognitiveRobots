import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
import time



## Setup mediapipe instance
def handpose(filename):
    cap = cv2.VideoCapture(filename)
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2,min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = hands.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            #print(id,lm)
                            h, w, c = image.shape
                            cx, cy = int(lm.x *w), int(lm.y*h)
                            #if id ==0:
                            cv2.circle(image, (cx,cy), 3, (255,0,255), cv2.FILLED)
                            mp_drawing.draw_landmarks(image, handLms, mp_hands.HAND_CONNECTIONS)
            except:
                pass

            
            #cTime = time.time()
            #fps = 1/(cTime-pTime)
            #pTime = cTime

            #cv2.putText(image, cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
            cv2.imshow("Image", image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            #cv2.imshow('Mediapipe Feed', image)
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":         
    handpose('arrange_right2_45.mp4')
