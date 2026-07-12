# Gesture Music Player using Hand Gestures

## Overview
This project is a Python-based gesture-controlled music player that uses a webcam to detect hand gestures with MediaPipe and control audio playback using Pygame.

## Features
- Real-time hand tracking
- Play/Resume music
- Pause/Unpause music
- Next song
- Previous song
- Displays current song on screen

## Technologies
- Python
- OpenCV
- MediaPipe
- Pygame

## Gesture Mapping
| Gesture | Action |
|---|---|
| Thumb up | Play |
| Fist | Pause/Unpause |
| Index + Middle | Next song |
| Index only | Previous song |

## Requirements
```
pip install opencv-python mediapipe pygame
```

## Usage
1. Add MP3/WAV files to the configured songs folder.
2. Run:
```bash
python hand_gesture.py
```
3. Allow webcam access.
4. Press **q** to quit.

## Project Workflow
Webcam → MediaPipe Hand Detection → Gesture Classification → Pygame Music Control

## Future Enhancements
- Volume control gestures
- Shuffle and repeat
- GUI playlist
- Dynamic music folder selection

## Author
Mohammed Aashik

## License
Educational use only.
