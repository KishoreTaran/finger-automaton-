import cv2
import mediapipe as mp
import time
from gpiozero import LED

led1 = LED("14")
led2 = LED("15")

# pip install python-time
# pip install opencv-python
# pip install mediapipe


mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
tipIds = [4, 8, 12, 16, 20]

# url = 'http://192.168.29.173:8080/video'    if you want to access cam through URL  # install ip webcame pro


video = cv2.VideoCapture(0)


def gpio14_on():
    led1.off()


def gpio_off():
    led1.on()
    led2.on()


def gpio15_on():
    led2.off()


with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        lmList = []
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                myHands = results.multi_hand_landmarks[0]
                for id, lm in enumerate(myHands.landmark):
                    h, w, c = image.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mp_draw.draw_landmarks(
                    image, hand_landmark, mp_hand.HAND_CONNECTIONS)
        fingers = []
        if len(lmList) != 0:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            total = fingers.count(1)

            if total == 0:
                cv2.putText(image, "All Relay OFF", (45, 375),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
                gpio_off()
            elif total == 1:
                cv2.putText(image, "Relay1 ON", (45, 375),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
                gpio14_on()
            elif total == 2:
                cv2.putText(image, "Relay2 ON", (45, 375),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
                gpio15_on()

            elif total == 3:
                cv2.putText(image, "Relay3 ON", (45, 375),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            elif total == 4:
                cv2.putText(image, "Relay4 ON", (45, 375),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            elif total == 5:
                cv2.putText(image, "Relay5 ON", (45, 375),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        cv2.imshow("AI Automation", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
video.release()
cv2.destroyAllWindows()
