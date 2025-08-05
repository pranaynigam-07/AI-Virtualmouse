# 🖱️ Smart Virtual Mouse with Hand Gestures

Control your computer using only hand gestures detected via webcam!  
This Python-based virtual mouse uses **OpenCV**, **MediaPipe**, and **PyAutoGUI** to simulate mouse movements, clicks, scrolling, dragging, and even screenshots — all with your hand.

---

## ✨ Features

- ✅ **Move cursor** using your hand
- ✅ **Left click** and **double click** gestures
- ✅ **Right click**
- ✅ **Drag & Drop** with pinch gesture
- ✅ **Scroll up/down**
- ✅ **Take screenshots** with a hand sign

---

## 🧠 Gesture Controls

| Gesture Description                        | Action             |
|-------------------------------------------|--------------------|
| Thumb, Index, Middle fingers up           | Move Cursor        |
| Index half-bent, Middle up                | Left Click / Double Click |
| Repeat above gesture quickly              | Double Click       |
| Middle half-bent, Index up                | Right Click        |
| Pinch (Thumb and Index tip close)         | Drag & Drop        |
| Index, Middle, Ring fingers up            | Scroll Up          |
| Index, Middle, Ring fingers half-bent     | Scroll Down        |
| All fingers half-bent                     | Take Screenshot    |

---

## 🖥️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/smart-virtual-mouse.git
cd smart-virtual-mouse
```
## 2. (Optional) Create a virtual environment
```bash 
python -m venv venv
```
# Activate it:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

## 3. Install dependencies
```bash
pip install -r requirements.txt
```
## 🚀 Run the Application
```bash
python smart_mouse.py
```
# Press q to quit the application.

## 🧪 Requirements
Python 3.7+
Webcam (for real-time hand tracking)

