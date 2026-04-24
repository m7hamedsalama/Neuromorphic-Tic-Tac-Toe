<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=00ffcc&height=200&section=header&text=Neuromorphic%20Tic-Tac-Toe&fontSize=50&fontColor=ffffff&animation=fadeIn" width="100%">
  
  <h3>🤖 A Touchless, AI-Driven Interactive Vision Studio 👁️</h3>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-red?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV">
    <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-00ffcc?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe">
    <img src="https://img.shields.io/badge/Streamlit-Web%20UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  </p>
</div>

---

## 🌌 Project Overview
**Neuromorphic Tic-Tac-Toe** is a cutting-edge proof-of-concept integrating **Computer Vision** and **Reinforcement Learning**. It allows users to play completely hands-free using real-time webcam tracking. 

The system acts as a live laboratory, visualizing the AI's decision-making process (Nodes Evaluated, Latency, and Memory building) directly through a highly responsive **Cyberpunk/Glassmorphism** Streamlit interface.

---

## 🎮 Live Demonstration (Touchless Gameplay)

> **Note for the Developer:** Record a 5-second video of you playing the game, convert it to a GIF (using ezgif.com), and replace the link below!

<div align="center">
  <img src="![Uploading AI_1-ezgif.com-video-to-gif-converter.gif…]()
" alt="Gameplay Demo Placeholder" width="600" style="border-radius: 15px;">
 
  <p><i>The system calculates the Euclidean Distance between the index and thumb to register a 'Pinch' click with zero latency.</i></p>
</div>

---

## 🧠 The AI Engine: Algorithms Under the Hood

This project does not rely on hardcoded rules; it compares two distinct branches of Artificial Intelligence:

### 1. The "Impossible" Agent (Classical AI)
* **Minimax Algorithm:** Simulates all possible future board states.
* **Alpha-Beta Pruning:** Drastically optimizes the search tree by eliminating mathematically inferior branches, ensuring the camera feed remains 100% unblocked during calculations.

### 2. The "Adaptive" Agent (Deep Q-Learning)
* **Reinforcement Learning:** The agent starts with zero knowledge and populates a `Q-Table` through trial and error.
* **Epsilon-Greedy Strategy:** Balances *Exploration* (random moves to discover new tactics) with *Exploitation* (using memory to win).
* **Auto-Train Matrix:** Simulates 5,000 matches in the background in seconds. The agent updates its memory using the simplified Bellman Equation:

$$Q(s, a) \leftarrow Q(s, a) + \alpha \left[ R + \gamma \max_{a'} Q(s', a') - Q(s, a) \right]$$

---

## ✨ System Architecture & Features

| Feature | Description |
| :--- | :--- |
| 👁️ **Touchless Interaction** | Zero physical contact required. Powered by `MediaPipe` 3D Hand Landmarks. |
| 📊 **Live Neural Analysis** | Real-time `Area Chart` rendering the AI's computational load & latency. |
| ⚡ **Non-Blocking Execution** | Optimized threading logic to ensure the webcam runs at max FPS without freezing. |
| 🎨 **Cyberpunk UI** | Immersive deep-space aesthetic with neon highlights built natively in `Streamlit`. |

---

## 🚀 Quick Start Guide

### Prerequisites
Ensure you have Python 3.11+ installed.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/MohamedSalama/Neuromorphic-Tic-Tac-Toe.git](https://github.com/MohamedSalama/Neuromorphic-Tic-Tac-Toe.git)
   cd Neuromorphic-Tic-Tac-Toe
2- Create and activate a virtual environment:
python -m venv myenv
# On Windows:
myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
Install the required libraries:

3- Install the required libraries:
pip install streamlit opencv-python mediapipe numpy
Launch the Vision Studio:

Bash
streamlit run app.py
   
