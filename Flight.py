import math
import cv2
import keyinput
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

def relall():
        keyinput.release_key('d')
        keyinput.release_key('w')
        keyinput.release_key('q')
        keyinput.release_key('s')
        keyinput.release_key('a')
        keyinput.release_key('z')
        keyinput.release_key('x')
        keyinput.release_key('c')
        keyinput.release_key('left')
        keyinput.release_key('right')
        keyinput.release_key('e')

# 0 For webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    imageHeight, imageWidth, _ = image.shape

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    co=[]
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS)
        for point in mp_hands.HandLandmark:
           if str(point) == "HandLandmark.WRIST":
              normalizedLandmark = hand_landmarks.landmark[point]
              pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                        normalizedLandmark.y,
                                                                                    imageWidth, imageHeight)

              try:
                co.append(list(pixelCoordinatesLandmark))
              except:
                  continue
    if len(co) == 2:
        xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2
        radius = 120
        try:
            m = (co[1][1] - co[0][1]) / (co[1][0] - co[0][0])
        except:
            continue
        a = 1 + m ** 2
        b = -2 * xm - 2 * co[0][0] * (m ** 2) + 2 * m * co[0][1] - 2 * m * ym
        c = xm ** 2 + (m ** 2) * (co[0][0] ** 2) + co[0][1] ** 2 + ym ** 2 - 2 * co[0][1] * ym - 2 * co[0][1] * co[0][
            0] * m + 2 * m * ym * co[0][0] - radius*radius
        xa = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        xb = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        ya = m * (xa - co[0][0]) + co[0][1]
        yb = m * (xb - co[0][0]) + co[0][1]

        cv2.circle(img=image, center=(int(325), int(275)), radius=80, color=(195, 255, 62), thickness=15)
        #cv2.ellipse(image, (int(xm), int(ym)), (100, 50), 360, 20, 160, 10, -1)
        cv2.circle(img=image, center=(int(xm), int(ym)), radius=30, color=(0, 0, 0), thickness=25)
        cv2.ellipse(image, (int(xa), int(ya)), (100, 50), 270, 20, 160, 10, -1)
        cv2.ellipse(image, (int(xb), int(yb)), (100, 50), 90, 20, 160, 10, -1)

        l = (int(math.sqrt((co[0][0] - co[1][0]) ** 2 * (co[0][1] - co[1][1]) ** 2)) - 150) // 2
        cv2.line(image, (int(xa), int(ya)), (int(xb), int(yb)), (0, 0, 0), 35)
        cv2.line(image, (int(325), int(275)), (int(xm), int(ym)), (0, 0, 0), 35)
        relall()
        cv2.circle(img=image, center=(int(co[0][0]), int(co[0][1])), radius=30, color=(0, 0, 0), thickness=25)
        if co[0][0] > co[1][0] and co[0][1]>co[1][1] and co[0][1] - co[1][1] > 65:
            # When the slope is negative, we turn left.
            keyinput.press_key('a')
            relall()
            print("a")
        elif co[1][0] > co[0][0] and co[1][1]> co[0][1] and co[1][1] - co[0][1] > 65:
            print("a")
            keyinput.press_key('a')
            relall()
        elif co[0][0] > co[1][0] and co[1][1]> co[0][1] and co[1][1] - co[0][1] > 65:
            print("d")
            keyinput.press_key('d')
            relall()
        elif co[1][0] > co[0][0] and co[0][1]> co[1][1] and co[0][1] - co[1][1] > 65:
            print("d")
            keyinput.press_key('d')
            relall()

        elif xm<270 and ym>300:
            keyinput.press_key('z')
            relall()
            print("z")
        elif xm>380 and 300> ym >250:
            print("Turn left.")
            keyinput.press_key('left')
            relall()
        elif xm>380 and ym <250:
            keyinput.press_key('e')
            relall()
            print("e")
        elif 270<xm<380 and ym<250:
            keyinput.press_key('w')
            relall()
            print("w")
        elif xm<270 and 250<ym<300:
            print("Turn right.")
            keyinput.press_key('right')
            relall()
        elif xm<270 and ym<250:
            print("q")
            keyinput.press_key('q')
            relall()
        elif xm<270 and 300< ym:
            print("z")
            keyinput.press_key('z')
            relall()
        elif 270<xm<380 and 300<ym:
            print("x")
            keyinput.press_key('x')
            relall()
        elif xm>380 and ym>300:
            keyinput.press_key('c')
            relall()
            print("c")
        else:
            print("stable")
            relall()
            cv2.putText(image, "keep straight", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    else:
        relall()
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))

# Flip the image horizontally for a selfie-view display.
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
cap.release()
