import cv2
import streamlit as st
import numpy as np
from game_logic import TicTacToeAI
from vision_module import HandTracker
import time

# ==========================================
# 1. Premium UI/UX (Keep same styles)
# ==========================================
st.set_page_config(page_title="Vision AI Studio", layout="wide", page_icon="🧿")

st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #050B14 0%, #0A192F 100%); color: #E6F1FF; }
    h1, h2, h3 { color: #64FFDA; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-shadow: 0 0 10px rgba(100,255,218,0.3); }
    div[data-testid="metric-container"] { 
        background: rgba(16, 32, 64, 0.6); backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 255, 218, 0.2); border-radius: 15px; padding: 20px; 
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover { transform: translateY(-5px); border-color: #64FFDA; }
    .stButton>button { 
        background: transparent; color: #64FFDA; border: 2px solid #64FFDA;
        border-radius: 10px; font-weight: bold; letter-spacing: 1px; transition: all 0.3s;
    }
    .stButton>button:hover { background: rgba(100, 255, 218, 0.1); box-shadow: 0 0 15px #64FFDA; transform: scale(1.02); }
</style>
""", unsafe_allow_html=True)

# Session States
if 'ai' not in st.session_state: st.session_state.ai = TicTacToeAI()
if 'tracker' not in st.session_state: st.session_state.tracker = HandTracker()
if 'scores' not in st.session_state: st.session_state.scores = {"Player": 0, "Agent": 0, "Draws": 0}
if 'stats_history' not in st.session_state: st.session_state.stats_history = []

if 'waiting_for_ai' not in st.session_state: st.session_state.waiting_for_ai = False
if 'ai_exec_time' not in st.session_state: st.session_state.ai_exec_time = 0
if 'game_over' not in st.session_state: st.session_state.game_over = False

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2083/2083213.png", width=100)
    st.title("⚙️ System Controls")
    user_symbol = st.radio("Select Your Symbol:", ["X", "O"], horizontal=True)
    ai_symbol = "O" if user_symbol == "X" else "X"
    starter = st.selectbox("First Move By:", ["Player", "Agent"])
    difficulty = st.selectbox("Intelligence Mode:", ["Impossible (Minimax)", "Learning (Q-Learning)", "Random (Easy)"])
    latency_sec = st.slider("Agent Response Latency (Seconds):", 0.0, 3.0, 0.5, 0.1)
    st.divider()
    cam_on = st.toggle("🎥 Activate Vision System", value=False)
    if st.button("🔄 Reset Battleground"):
        st.session_state.ai = TicTacToeAI()
        st.session_state.game_over = False
        st.session_state.stats_history = []
        st.rerun()

# Dashboard
st.title("🕹️ Neuromorphic Tic-Tac-Toe")
st.caption("Powered by Minimax & MediaPipe Vision & Deep Q-Learning & Random")

c1, c2, c3 = st.columns(3)
c1.metric("PLAYER WINS", st.session_state.scores["Player"], f"Symbol: {user_symbol}")
c2.metric("AGENT WINS", st.session_state.scores["Agent"], f"Symbol: {ai_symbol}", delta_color="inverse")
c3.metric("MATCH DRAWS", st.session_state.scores["Draws"], "Tie")

tab_vision, tab_analysis, tab_tutorial = st.tabs(["👁️ Vision Arena", "🧠 Neural Analysis", "📖 How to Play"])

with tab_tutorial:
    st.markdown("""
    ### 🎮 How to Play
    1. **Hand Presence:** Ensure your right hand is visible in the camera frame.
    2. **Pointing:** Use your **Index Finger** to hover over the grid on the screen.
    3. **Action:** Perform a **Pinch Gesture** (Index + Thumb close together) to confirm your move.
    4. **Reinforcement:** In 'Learning Mode', the agent learns from its mistakes. If you beat it once with a trick, it won't fall for it again!
    """)
with tab_analysis:
    st.subheader("Performance & Computational Analysis")
    chart_placeholder = st.empty()
    if st.session_state.stats_history:
        chart_placeholder.area_chart(st.session_state.stats_history)
        st.caption("X-Axis: Moves | Y-Axis: Intelligence Processing Score")
    else:
        st.info("Play moves to generate neural data.")

with tab_vision:
    # 🚨 مكان رسالة الفوز/الخسارة الجديدة
    game_status_alert = st.empty()
    frame_placeholder = st.empty()
    
    if cam_on:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while cap.isOpened() and cam_on:
            ret, frame = cap.read()
            if not ret: break
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            frame, pos, clicked = st.session_state.tracker.process_frame(frame)
            frame = st.session_state.tracker.draw_grid(frame)
            
            # AI Logic
            if st.session_state.waiting_for_ai and time.time() >= st.session_state.ai_exec_time:
                m = st.session_state.ai.get_best_move(difficulty, ai_symbol, user_symbol)
                if m != -1: 
                    st.session_state.last_ai_state = "".join(st.session_state.ai.board)
                    st.session_state.last_ai_move = m
                    st.session_state.ai.make_move(m, ai_symbol)
                    
                    val = st.session_state.ai.nodes_evaluated if difficulty == "Impossible (Minimax)" else st.session_state.ai.response_time * 10
                    st.session_state.stats_history.append(val)
                    with tab_analysis: chart_placeholder.area_chart(st.session_state.stats_history)

                if st.session_state.ai.check_winner(st.session_state.ai.board, ai_symbol):
                    st.session_state.scores["Agent"] += 1
                    st.session_state.game_over = True
                    if difficulty == "Learning (Q-Learning)": 
                        st.session_state.ai.train(st.session_state.last_ai_state, st.session_state.last_ai_move, 20)
                elif st.session_state.ai.is_draw(st.session_state.ai.board):
                    st.session_state.scores["Draws"] += 1
                    st.session_state.game_over = True
                st.session_state.waiting_for_ai = False

            elif clicked and pos and not st.session_state.game_over and not st.session_state.waiting_for_ai:
                sq = st.session_state.tracker.get_grid_position(pos[0], pos[1], w, h)
                if st.session_state.ai.make_move(sq, user_symbol):
                    if st.session_state.ai.check_winner(st.session_state.ai.board, user_symbol):
                        st.session_state.scores["Player"] += 1
                        st.session_state.game_over = True
                        if difficulty == "Learning (Q-Learning)" and st.session_state.last_ai_state: 
                            st.session_state.ai.train(st.session_state.last_ai_state, st.session_state.last_ai_move, -20)
                    elif st.session_state.ai.is_draw(st.session_state.ai.board):
                        st.session_state.scores["Draws"] += 1
                        st.session_state.game_over = True
                    else:
                        st.session_state.waiting_for_ai = True
                        st.session_state.ai_exec_time = time.time() + latency_sec

            # Render Grid X-O
            for i, mark in enumerate(st.session_state.ai.board):
                if mark != ' ':
                    r, c = divmod(i, 3)
                    color = (100, 255, 218) if mark == user_symbol else (255, 64, 129)
                    cv2.putText(frame, mark, (c*w//3 + 60, r*h//3 + 110), cv2.FONT_HERSHEY_DUPLEX, 2, color, 4)

            # --- ON-SCREEN RESULTS & ALERTS ---
            if st.session_state.game_over:
                overlay = frame.copy()
                cv2.rectangle(overlay, (0, h//2-70), (w, h//2+70), (10, 25, 47), -1)
                cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
                
                # 🚨 هنا بتظهر الرسائل زي ما طلبت بالظبط
                if st.session_state.ai.check_winner(st.session_state.ai.board, user_symbol):
                    cv2.putText(frame, "PLAYER WINS!", (w//2-200, h//2+20), cv2.FONT_HERSHEY_DUPLEX, 2, (100, 255, 218), 4)
                    game_status_alert.success("🎉 مبروك! أنا كسبت (You Won)")
                elif st.session_state.ai.check_winner(st.session_state.ai.board, ai_symbol):
                    cv2.putText(frame, "AGENT WINS!", (w//2-180, h//2+20), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 64, 129), 4)
                    game_status_alert.error("🤖 الأجنت هو اللي كسب (Agent Won)")
                else:
                    cv2.putText(frame, "IT'S A DRAW!", (w//2-180, h//2+20), cv2.FONT_HERSHEY_DUPLEX, 2, (148, 163, 184), 4)
                    game_status_alert.warning("🤝 تعادل (Draw)")

            frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        cap.release()