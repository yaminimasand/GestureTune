import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.set_page_config(page_title="Gesture Volume Control", page_icon="🎚️", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stApp {
        background: radial-gradient(circle at 30% 30%, #1b2735, #090a0f);
    }
    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        color: #7bdcb5;
        text-shadow: 0px 0px 10px #7bdcb5;
    }
    .subtext {
        text-align: center;
        color: #d4d4dc;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🎚️ AI Hand Volume Controller</div>", unsafe_allow_html=True)
st.markdown("<div class='subtext'>Control system volume using hand gestures via your webcam</div>",
            unsafe_allow_html=True)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils


class HandGestureTransformer(VideoTransformerBase):
    def __init__(self):
        self.hands = mp_hands.Hands()
        self.volume_state = "Neutral"

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_img)

        h, w, _ = img.shape
        x1 = y1 = x2 = y2 = 0

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark

                x1, y1 = int(landmarks[8].x * w), int(landmarks[8].y * h)
                x2, y2 = int(landmarks[4].x * w), int(landmarks[4].y * h)

                cv2.circle(img, (x1, y1), 8, (0, 255, 255), -1)
                cv2.circle(img, (x2, y2), 8, (0, 0, 255), -1)
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 / 4

                if distance > 50:
                    pyautogui.press('volumeup')
                    self.volume_state = "🔊 Volume Up"
                    cv2.putText(img, "Volume Up", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                else:
                    pyautogui.press('volumedown')
                    self.volume_state = "🔉 Volume Down"
                    cv2.putText(img, "Volume Down", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        return img

webrtc_streamer(
    key="gesture-control",
    video_transformer_factory=HandGestureTransformer,
    media_stream_constraints={"video": True, "audio": False},
)

st.sidebar.markdown("## ⚙️ Settings")
st.sidebar.info("""
🖐 **How to Use:**
1. Show your hand in front of webcam.  
2. Move **index finger (id=8)** and **thumb (id=4)** closer → 🔉 Decrease volume.  
3. Move them apart → 🔊 Increase volume.  
4. Press **ESC** or stop webcam to exit.

💡 Tip: Works best in bright lighting.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("👩‍💻 *Built by Yamini Masand*")

