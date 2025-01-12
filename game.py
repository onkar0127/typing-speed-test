import streamlit as st
import numpy as np
import time
from streamlit.components.v1 import html

def inject_custom_css():
    return st.markdown("""
        <style>
            .stButton button {
                width: 100px;
                height: 50px;
                margin: 10px;
                font-size: 20px;
                font-weight: bold;
            }
            .game-container {
                width: 100%;
                max-width: 800px;
                margin: 0 auto;
            }
            .control-panel {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 20px 0;
            }
            .score-display {
                font-size: 24px;
                text-align: center;
                margin: 20px 0;
            }
            @media (max-width: 600px) {
                .stButton button {
                    width: 80px;
                    height: 40px;
                    font-size: 16px;
                }
            }
        </style>
    """, unsafe_allow_html=True)

def init_game_state():
    if 'ball_pos' not in st.session_state:
        st.session_state.ball_pos = [50, 0]  # [x, y]
        st.session_state.paddle_pos = 45
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.ball_speed = 3
        st.session_state.last_update = time.time()
        st.session_state.high_score = 0
        st.session_state.game_paused = False

def move_paddle(direction):
    move_speed = 5
    if direction == 'left':
        st.session_state.paddle_pos = max(5, st.session_state.paddle_pos - move_speed)
    else:
        st.session_state.paddle_pos = min(95, st.session_state.paddle_pos + move_speed)

def create_game():
    init_game_state()
    inject_custom_css()

    # Game container
    game_container = st.empty()

    # Score display
    score_container = st.markdown(
        f'<div class="score-display">Score: {st.session_state.score} | High Score: {st.session_state.high_score}</div>',
        unsafe_allow_html=True
    )

    # Control buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button('←'):
            move_paddle('left')
    with col2:
        if st.button('→'):
            move_paddle('right')
    with col3:
        if st.button('Pause'):
            st.session_state.game_paused = not st.session_state.game_paused
    with col4:
        if st.button('Reset'):
            st.session_state.clear()
            st.experimental_rerun()

    # Keyboard controls
    keyboard_js = """
    <script>
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            document.querySelector('button:contains("←")').click();
        } else if (e.key === 'ArrowRight') {
            document.querySelector('button:contains("→")').click();
        } else if (e.key === ' ') {
            document.querySelector('button:contains("Pause")').click();
        }
    });
    </script>
    """
    st.components.v1.html(keyboard_js, height=0)

    # Game loop
    while not st.session_state.game_over:
        if not st.session_state.game_paused:
            current_time = time.time()
            delta_time = current_time - st.session_state.last_update

            # Update ball position
            st.session_state.ball_pos[1] += st.session_state.ball_speed * delta_time

            # Check for collision with paddle
            if st.session_state.ball_pos[1] >= 90:
                if abs(st.session_state.ball_pos[0] - st.session_state.paddle_pos) < 10:
                    # Ball caught
                    st.session_state.score += 1
                    if st.session_state.score > st.session_state.high_score:
                        st.session_state.high_score = st.session_state.score
                    st.session_state.ball_pos = [np.random.randint(10, 90), 0]
                    st.session_state.ball_speed += 0.2  # Smaller speed increase for better difficulty curve
                else:
                    # Game over
                    st.session_state.game_over = True

            # Draw game state
            game_state = f"""
            <div class="game-container">
                <div style="width: 100%; height: 400px; background-color: #1a1a1a; position: relative; border-radius: 10px; overflow: hidden;">
                    <div style="position: absolute; left: {st.session_state.ball_pos[0]}%; top: {st.session_state.ball_pos[1]}%; 
                                width: 20px; height: 20px; background-color: #ff4b4b; border-radius: 50%;
                                box-shadow: 0 0 10px #ff4b4b;"></div>
                    <div style="position: absolute; left: {st.session_state.paddle_pos}%; bottom: 10px; 
                                width: 80px; height: 10px; background-color: #4bb4ff; transform: translateX(-50%);
                                border-radius: 5px; box-shadow: 0 0 10px #4bb4ff;"></div>
                </div>
            </div>
            """
            game_container.markdown(game_state, unsafe_allow_html=True)
            score_container.markdown(
                f'<div class="score-display">Score: {st.session_state.score} | High Score: {st.session_state.high_score}</div>',
                unsafe_allow_html=True
            )

            st.session_state.last_update = current_time

        time.sleep(0.016)  # Roughly 60 FPS

    # Game over screen
    game_over_html = f"""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #ff4b4b;">Game Over!</h1>
        <h2>Final Score: {st.session_state.score}</h2>
        <h3>High Score: {st.session_state.high_score}</h3>
    </div>
    """
    st.markdown(game_over_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again", key="play_again"):
            st.session_state.clear()
            st.experimental_rerun()
    with col2:
        if st.button("Quit", key="quit"):
            st.stop()

def main():
    st.set_page_config(page_title="Ball Catching Game", layout="wide")

    st.markdown("""
        <h1 style='text-align: center; color: #4bb4ff;'>Ball Catching Game</h1>
        <div style='text-align: center; margin-bottom: 20px;'>
            <p>Use ← and → arrow keys or buttons to move the paddle</p>
            <p>Press Space to pause the game</p>
        </div>
    """, unsafe_allow_html=True)

    create_game()

if __name__ == "__main__":
    main()