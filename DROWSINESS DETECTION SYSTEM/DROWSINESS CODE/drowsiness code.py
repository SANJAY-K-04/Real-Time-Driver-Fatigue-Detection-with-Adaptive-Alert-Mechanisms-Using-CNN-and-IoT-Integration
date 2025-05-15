import os
import dlib
import cv2
import imutils
import serial
import time
from scipy.spatial import distance as dist
from imutils import face_utils

# Constants
EAR_THRESHOLD = 0.2
SHAPE_PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
DROWSY_TIME = 1.5  # seconds
BRAKE_TIME = 1.0   # seconds (after drowsy alert)

# Check if shape predictor file exists
if not os.path.exists(SHAPE_PREDICTOR_PATH):
    print(f"Error: Shape predictor file not found at {SHAPE_PREDICTOR_PATH}")
    exit()

# Load face detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)

# Get eye landmark indexes
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# Function to calculate Eye Aspect Ratio
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

# Arduino setup
ARDUINO_PORT = 'COM9'  # Change COM port if needed
BAUD_RATE = 9600
try:
    arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE)
    time.sleep(2)
    print(f"Connected to Arduino on {ARDUINO_PORT}")
except serial.SerialException:
    print(f"Warning: Could not connect to Arduino on {ARDUINO_PORT}")
    arduino = None

# Camera setup
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# State variables
eye_closed_start = None
drowsy_alert_triggered = False
brake_applied = False

# Main loop
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    frame = imutils.resize(frame, width=850)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray)

    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        if ear < EAR_THRESHOLD:
            # Eye closed
            if eye_closed_start is None:
                eye_closed_start = time.time()
                drowsy_alert_triggered = False
                brake_applied = False

            closed_duration = time.time() - eye_closed_start

            # Timer display
            cv2.putText(frame, f"Eye Closed: {closed_duration:.2f}s", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Trigger drowsy alert at 1.5s
            if closed_duration >= DROWSY_TIME and not drowsy_alert_triggered:
                cv2.putText(frame, "DROWSY ALERT!", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if arduino:
                    arduino.write(b'z')  # Custom signal for buzzer ON
                drowsy_alert_triggered = True

            # Apply brake at 2s (1.5 + 1.0)
            if closed_duration >= DROWSY_TIME + BRAKE_TIME:
                if not brake_applied:
                    if arduino:
                        arduino.write(b'a')  # Brake signal
                    brake_applied = True

            # Show "BRAKE APPLIED!" if brake was applied
            if brake_applied:
                cv2.putText(frame, "BRAKE APPLIED!", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        else:
            # Eye open
            if eye_closed_start is not None:
                if arduino:
                    arduino.write(b'b')  # Resume signal
                eye_closed_start = None
                drowsy_alert_triggered = False
                brake_applied = False

            # Optional: Show "Driver Awake" message
            cv2.putText(frame, "Driver Awake", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Draw eye contours
        cv2.drawContours(frame, [cv2.convexHull(leftEye)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [cv2.convexHull(rightEye)], -1, (0, 255, 0), 1)

    # Display the frame
    cv2.imshow("Drowsiness Detector", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cam.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
