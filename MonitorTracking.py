import math
import threading
import time
from collections import deque

import cv2
import keyboard
import mediapipe as mp
import numpy as np
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

MONITOR_WIDTH, MONITOR_HEIGHT = pyautogui.size()

SMOOTHING_FRAMES = 5
MOUSE_UPDATE_INTERVAL = 0.008
MAX_FACE_MOVE_X = 0.14
MAX_FACE_MOVE_Y = 0.12
MAX_YAW_DEG = 16.0
MAX_PITCH_DEG = 12.0
MOVE_WEIGHT = 0.75
POSE_WEIGHT = 0.25
DEADZONE = 0.025
CURVE_EXPONENT = 1.65
BASE_SPEED_X = 42.0
BASE_SPEED_Y = 34.0
BOOST_SPEED_X = 95.0
BOOST_SPEED_Y = 80.0
DRAG_WHEN_IDLE = 0.82
MAX_DELTA_X = 120
MAX_DELTA_Y = 100

FACE_OUTLINE_INDICES = [
    10, 338, 297, 332, 284, 251, 389, 356,
    454, 323, 361, 288, 397, 365, 379, 378,
    400, 377, 152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127, 162, 21,
    54, 103, 67, 109
]

LANDMARKS = {
    "left": 234,
    "right": 454,
    "top": 10,
    "bottom": 152,
    "nose": 1,
}

mouse_control_enabled = True
mouse_lock = threading.Lock()
mouse_target = list(pyautogui.position())
mouse_velocity = np.array([0.0, 0.0], dtype=np.float32)

calibration_face_center = None
calibration_yaw = 0.0
calibration_pitch = 0.0

face_center_history = deque(maxlen=SMOOTHING_FRAMES)
yaw_history = deque(maxlen=SMOOTHING_FRAMES)
pitch_history = deque(maxlen=SMOOTHING_FRAMES)

latest_status_text = "Waiting for face..."

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)


def open_camera():
    for index in (0, 1, 2):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
        cap.release()
    return None


cap = open_camera()
if cap is None:
    raise RuntimeError("Kamera tidak ditemukan. Coba ganti index webcam ke 0/1/2.")


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def safe_normalize(vector, eps=1e-6):
    norm = np.linalg.norm(vector)
    if norm < eps:
        return None
    return vector / norm


def landmark_to_np(landmark, width, height):
    return np.array(
        [landmark.x * width, landmark.y * height, landmark.z * width],
        dtype=np.float32,
    )


def project(point_3d):
    return int(point_3d[0]), int(point_3d[1])


def shape_input(value):
    value = clamp(value, -1.0, 1.0)
    if abs(value) < DEADZONE:
        return 0.0

    scaled = (abs(value) - DEADZONE) / (1.0 - DEADZONE)
    curved = scaled ** CURVE_EXPONENT
    return math.copysign(curved, value)


def mouse_mover():
    global mouse_velocity

    while True:
        if mouse_control_enabled:
            with mouse_lock:
                target_x, target_y = mouse_target
            pyautogui.moveTo(int(target_x), int(target_y), duration=0)
        time.sleep(MOUSE_UPDATE_INTERVAL)


def update_cursor(control_x, control_y):
    global mouse_velocity

    accel_x = BASE_SPEED_X * control_x + BOOST_SPEED_X * (abs(control_x) ** 1.7) * np.sign(control_x)
    accel_y = BASE_SPEED_Y * control_y + BOOST_SPEED_Y * (abs(control_y) ** 1.7) * np.sign(control_y)

    if control_x == 0.0:
        mouse_velocity[0] *= DRAG_WHEN_IDLE
    else:
        mouse_velocity[0] = accel_x

    if control_y == 0.0:
        mouse_velocity[1] *= DRAG_WHEN_IDLE
    else:
        mouse_velocity[1] = accel_y

    mouse_velocity[0] = clamp(mouse_velocity[0], -MAX_DELTA_X, MAX_DELTA_X)
    mouse_velocity[1] = clamp(mouse_velocity[1], -MAX_DELTA_Y, MAX_DELTA_Y)

    current_x, current_y = pyautogui.position()
    next_x = clamp(current_x + mouse_velocity[0], 0, MONITOR_WIDTH - 1)
    next_y = clamp(current_y + mouse_velocity[1], 0, MONITOR_HEIGHT - 1)

    with mouse_lock:
        mouse_target[0] = int(next_x)
        mouse_target[1] = int(next_y)


def draw_status(frame, text, color=(0, 255, 0)):
    cv2.rectangle(frame, (10, 10), (590, 110), (0, 0, 0), -1)
    cv2.putText(frame, text, (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA)
    cv2.putText(
        frame,
        "c = calibrate | f7 = on/off mouse | q = quit",
        (20, 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )


threading.Thread(target=mouse_mover, daemon=True).start()

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Frame kamera gagal dibaca.")
            break

        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        landmarks_frame = np.zeros_like(frame)
        results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_face_landmarks:
            face_landmarks = results.multi_face_landmarks[0].landmark

            for index, landmark in enumerate(face_landmarks):
                point = landmark_to_np(landmark, width, height)
                px, py = int(point[0]), int(point[1])
                if 0 <= px < width and 0 <= py < height:
                    color = (150, 150, 150) if index in FACE_OUTLINE_INDICES else (0, 170, 255)
                    cv2.circle(landmarks_frame, (px, py), 2, color, -1)

            key_points = {}
            for name, landmark_index in LANDMARKS.items():
                point = landmark_to_np(face_landmarks[landmark_index], width, height)
                key_points[name] = point
                cv2.circle(frame, project(point), 4, (0, 0, 0), -1)

            left = key_points["left"]
            right = key_points["right"]
            top = key_points["top"]
            bottom = key_points["bottom"]
            nose = key_points["nose"]

            right_axis = safe_normalize(right - left)
            up_axis = safe_normalize(top - bottom)

            if right_axis is not None and up_axis is not None:
                forward_axis = safe_normalize(np.cross(right_axis, up_axis))
                if forward_axis is not None:
                    forward_axis = -forward_axis
                    raw_yaw = math.degrees(math.atan2(forward_axis[0], -forward_axis[2]))
                    raw_pitch = math.degrees(math.atan2(forward_axis[1], -forward_axis[2]))

                    face_center = np.array([nose[0] / width, nose[1] / height], dtype=np.float32)

                    if calibration_face_center is None:
                        calibration_face_center = face_center.copy()
                        calibration_yaw = raw_yaw
                        calibration_pitch = raw_pitch

                    face_center_history.append(face_center)
                    yaw_history.append(raw_yaw)
                    pitch_history.append(raw_pitch)

                    smooth_face_center = np.mean(np.array(face_center_history), axis=0)
                    smooth_yaw = float(np.mean(np.array(yaw_history)))
                    smooth_pitch = float(np.mean(np.array(pitch_history)))

                    face_offset = smooth_face_center - calibration_face_center
                    yaw_offset = smooth_yaw - calibration_yaw
                    pitch_offset = smooth_pitch - calibration_pitch

                    face_input_x = clamp(face_offset[0] / MAX_FACE_MOVE_X, -1.0, 1.0)
                    face_input_y = clamp(face_offset[1] / MAX_FACE_MOVE_Y, -1.0, 1.0)
                    pose_input_x = clamp(yaw_offset / MAX_YAW_DEG, -1.0, 1.0)
                    pose_input_y = clamp(pitch_offset / MAX_PITCH_DEG, -1.0, 1.0)

                    control_x = shape_input(MOVE_WEIGHT * face_input_x + POSE_WEIGHT * pose_input_x)
                    control_y = shape_input(MOVE_WEIGHT * face_input_y + POSE_WEIGHT * pose_input_y)

                    if mouse_control_enabled:
                        update_cursor(control_x, control_y)

                    center_px = int(calibration_face_center[0] * width)
                    center_py = int(calibration_face_center[1] * height)
                    nose_px = int(smooth_face_center[0] * width)
                    nose_py = int(smooth_face_center[1] * height)

                    cv2.circle(frame, (center_px, center_py), 10, (255, 255, 255), 2)
                    cv2.circle(frame, (nose_px, nose_py), 10, (0, 255, 0), 2)
                    cv2.line(frame, (center_px, center_py), (nose_px, nose_py), (0, 255, 0), 2)

                    status = (
                        f"Mouse {'ON' if mouse_control_enabled else 'OFF'} | "
                        f"move=({control_x:+.2f}, {control_y:+.2f}) | "
                        f"yaw={yaw_offset:+.1f} | pitch={pitch_offset:+.1f}"
                    )
                    latest_status_text = status
                    draw_status(frame, status)
                else:
                    draw_status(frame, "Forward axis gagal dihitung", (0, 165, 255))
            else:
                draw_status(frame, "Face axis gagal dihitung", (0, 165, 255))
        else:
            mouse_velocity *= 0.7
            draw_status(frame, "Wajah tidak terdeteksi", (0, 0, 255))

        cv2.imshow("Head Tracking Mouse", frame)
        cv2.imshow("Facial Landmarks", landmarks_frame)

        if keyboard.is_pressed("f7"):
            mouse_control_enabled = not mouse_control_enabled
            print(f"[Mouse Control] {'Enabled' if mouse_control_enabled else 'Disabled'}")
            time.sleep(0.3)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        if key == ord("c") and results.multi_face_landmarks:
            calibration_face_center = smooth_face_center.copy()
            calibration_yaw = smooth_yaw
            calibration_pitch = smooth_pitch
            mouse_velocity[:] = 0.0
            print("[Calibration] Posisi netral wajah berhasil disimpan.")
            time.sleep(0.2)

finally:
    cap.release()
    face_mesh.close()
    cv2.destroyAllWindows()

