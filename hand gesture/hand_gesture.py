import cv2
import mediapipe as mp
import time
import os
import pygame

# Path to your music folder (unzipped songs.zip here)
MUSIC_FOLDER = r"D:\clg project\songs"

# Ensure songs folder exists
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)
    print(f"⚠️ Created empty folder '{MUSIC_FOLDER}'. Please add MP3/WAV files into it.")

# Load all songs
playlist = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith((".mp3", ".wav"))]
playlist.sort()

if not playlist:
    print(f"❌ No songs found in '{MUSIC_FOLDER}' folder. Add some MP3/WAV files and restart.")

current_index = 0

# Initialize pygame mixer
pygame.mixer.init()
if playlist:
    pygame.mixer.music.load(playlist[current_index])

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

last_action_time = {"PLAY": 0, "PAUSE": 0, "NEXT": 0, "PREV": 0}
cooldown = 1.0  # seconds

cap = cv2.VideoCapture(0)

def fingers_up(landmarks):
    fingers = []
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    tip_ids = [8, 12, 16, 20]
    pip_ids = [6, 10, 14, 18]

    for tip, pip in zip(tip_ids, pip_ids):
        if landmarks[tip].y < landmarks[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def classify_gesture(landmarks):
    f_up = fingers_up(landmarks)
    now = time.time()

    if f_up == [1, 0, 0, 0, 0] and now - last_action_time["PLAY"] > cooldown:
        last_action_time["PLAY"] = now
        return "PLAY"

    if f_up == [0, 0, 0, 0, 0] and now - last_action_time["PAUSE"] > cooldown:
        last_action_time["PAUSE"] = now
        return "PAUSE"

    if f_up == [0, 1, 1, 0, 0] and now - last_action_time["NEXT"] > cooldown:
        last_action_time["NEXT"] = now
        return "NEXT"

    if f_up == [0, 1, 0, 0, 0] and now - last_action_time["PREV"] > cooldown:
        last_action_time["PREV"] = now
        return "PREV"

    return None

print("Press 'q' to quit.")
print("Use hand gestures in front of the webcam to control local songs.")

paused = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_song = os.path.basename(playlist[current_index]) if playlist else "No songs found"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = classify_gesture(hand_landmarks.landmark)

            if gesture:
                cv2.putText(frame, f"Gesture: {gesture}", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if gesture == "PLAY":
                print("▶ Play/Resume")
                if playlist:
                    if not pygame.mixer.music.get_busy() or paused:
                        pygame.mixer.music.play()
                        paused = False

            elif gesture == "PAUSE":
                print("⏸ Pause/Unpause")
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    paused = True
                else:
                    pygame.mixer.music.unpause()
                    paused = False

            elif gesture == "NEXT":
                if playlist:
                    print("⏭ Next Song")
                    current_index = (current_index + 1) % len(playlist)
                    pygame.mixer.music.load(playlist[current_index])
                    pygame.mixer.music.play()
                    current_song = os.path.basename(playlist[current_index])

            elif gesture == "PREV":
                if playlist:
                    print("⏮ Previous Song")
                    current_index = (current_index - 1) % len(playlist)
                    pygame.mixer.music.load(playlist[current_index])
                    pygame.mixer.music.play()
                    current_song = os.path.basename(playlist[current_index])

    # Display current song on screen
    cv2.putText(frame, f"Now Playing: {current_song}", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("Gesture Music Player", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.mixer.music.stop()





              

