import cv2
import mediapipe as mp
import serial
import time

# ---------- SERIAL ----------
SERIAL_PORT = 'COM4'   # change if needed
BAUD_RATE = 115200

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# ---------- MEDIAPIPE ----------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

last_sent = ""
last_time = 0

# ---------- FINGER STATES ----------
def finger_states(hand_landmarks):
    """
    True  = finger UP
    False = finger DOWN
    Order: Thumb, Index, Middle, Ring, Pinky.
    """
    tips = [4, 8, 12, 16, 20]
    pips = [2, 6, 10, 14, 18]

    states = []

    # Thumb (x-axis because of hand orientation)
    thumb_tip = hand_landmarks.landmark[tips[0]]
    thumb_ip  = hand_landmarks.landmark[pips[0]]
    states.append(thumb_tip.x < thumb_ip.x)

    # Other fingers (y-axis)
    for i in range(1, 5):
        tip = hand_landmarks.landmark[tips[i]]
        pip = hand_landmarks.landmark[pips[i]]
        states.append(tip.y < pip.y)

    return states

# ---------- ASL DETECTION ----------
def detect_asl(states):
    thumb, indexF, middleF, ringF, pinky = states

    # ASL A
    if thumb and not indexF and not middleF and not ringF and not pinky:
        return "A"

    # ASL B
    if not thumb and indexF and middleF and ringF and pinky:
        return "B"
    
     # ASL D
    if not thumb and indexF and not middleF and not ringF and not pinky:
        return "D"
    
    # ASL F
    if not thumb and not indexF and middleF and ringF and pinky:
        return "F"
    
    # ASL I
    if not thumb and not indexF and not middleF and not ringF and pinky:
        return "I"
    
    # ASL L
    if  thumb and  indexF and not middleF and not ringF and not pinky:
        return "L"
    
    # ASL S
    if  not thumb and  not indexF and not middleF and not ringF and not pinky:
        return "S"
    
    # ASL V
    if  not thumb and  indexF and middleF and not ringF and not pinky:
        return "V"
    
     # ASL W
    if  not thumb and  indexF and middleF and ringF and not pinky:
        return "W"
    
     # ASL Y
    if  thumb and  not indexF and not middleF and not ringF and pinky:
        return "Y"
    return None

# ---------- MAIN LOOP ----------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        states = finger_states(hand)
        letter = detect_asl(states)

        if letter:
            now = time.time()
            if letter != last_sent or now - last_time > 1:
                arduino.write((letter + "\n").encode())
                last_sent = letter
                last_time = now

            cv2.putText(frame, f"ASL Letter: {letter}",
                        (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 0), 3)

        # Debug display (optional)
        labels = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        for i, name in enumerate(labels):
            cv2.putText(frame,
                        f"{name}: {'UP' if states[i] else 'DOWN'}",
                        (20, 100 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0,255,0) if states[i] else (0,0,255),
                        2)

    cv2.imshow("ASL Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
