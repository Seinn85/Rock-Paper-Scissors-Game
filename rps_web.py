import streamlit as st
import random
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit.components.v1 as components
import json

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

def store_result(player_choice, computer_choice, result):
    if not supabase:
        st.warning("Supabase not configured. Skipping result storage.")
        return
    data = {
        "player_choice": player_choice,
        "computer_choice": computer_choice,
        "result": result
    }
    try:
        supabase.table("rps_results").insert(data).execute()
    except Exception as e:
        st.error(f"Failed to store result in Supabase: {e}")

def get_computer_choice():
    return random.choice(["Rock", "Paper", "Scissors"])

def determine_winner(player, computer):
    if player == computer:
        return "Draw"
    elif (
        (player == "Rock" and computer == "Scissors") or
        (player == "Scissors" and computer == "Paper") or
        (player == "Paper" and computer == "Rock")
    ):
        return "Win"
    else:
        return "Lose"

st.set_page_config(page_title="Rock-Paper-Scissors", page_icon="✊✋✌️", layout="centered")
st.markdown("""
    <style>
    body {
        background: linear-gradient(120deg, #43cea2 0%, #6a11cb 100%) !important;
    }
    .stApp {
        background: linear-gradient(120deg, #43cea2 0%, #6a11cb 100%) !important;
        min-height: 100vh;
    }
    .big-button button {
        font-size: 2rem !important;
        height: 80px !important;
        width: 100% !important;
        margin-bottom: 10px !important;
        border-radius: 16px !important;
        background: linear-gradient(135deg, #ffb347 0%, #ff7675 100%) !important;
        color: #232526 !important;
        font-weight: bold !important;
        box-shadow: 0 3px 12px rgba(255, 200, 50, 0.25);
        transition: 0.2s;
    }
    .big-button button:hover {
        background: linear-gradient(135deg, #ffcc33 0%, #ffb347 100%) !important;
        transform: scale(1.05);
    }
    .history-entry {
        opacity: .7;
        margin-bottom: .2em;
    }
    .history-entry:last-child {
        opacity: 1;
        font-weight: 700;
        color: #ffe066;
    }
    .reset-btn button, .reset-btn > div > button {
        background: linear-gradient(90deg, #ff7675 0%, #74b9ff 100%) !important;
        color: #fff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        height: 24px !important;
        min-height: 24px !important;
        font-size: 0.78rem !important;
        margin: 0 !important;
        padding: 0 10px !important;
        min-width: 60px !important;
        box-shadow: 0 2px 8px rgba(116,185,255,0.12);
        transition: 0.2s;
        line-height: 1.1 !important;
    }
    .reset-btn button:hover {
        background: linear-gradient(90deg, #74b9ff 0%, #ff7675 100%) !important;
        color: #232526 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Language dictionary
LANGS = {
    'English': {
        'title': "Rock Paper Scissors",
        'choose_move': "Choose your move:",
        'rock': "Rock",
        'paper': "Paper",
        'scissors': "Scissors",
        'win': "Win",
        'lose': "Lose",
        'draw': "Draw",
        'score': "Score",
        'reset': "Reset Score",
        'recent_games': "Recent Games:",
        'you': "You",
        'computer': "Computer",
        'result': "Result",
        'wins': "Wins",
        'losses': "Losses",
        'draws': "Draws",
        'thinking': "The computer is thinking..."
    },
    '日本語': {
        'title': "じゃんけん (グー・チョキ・パー)",
        'choose_move': "手を選んでください：",
        'rock': "グー",
        'paper': "パー",
        'scissors': "チョキ",
        'win': "勝ち",
        'lose': "負け",
        'draw': "引き分け",
        'score': "スコア",
        'reset': "リセット",
        'recent_games': "最近の対戦：",
        'you': "あなた",
        'computer': "コンピューター",
        'result': "結果",
        'wins': "勝ち",
        'losses': "負け",
        'draws': "引き分け",
        'thinking': "コンピューターが考えています..."
    }
}

if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

lang = st.sidebar.radio('Language / 言語', list(LANGS.keys()), index=list(LANGS.keys()).index(st.session_state.lang))
st.session_state.lang = lang
L = LANGS[lang]

st.markdown(f"<h1 style='text-align:center; margin-bottom:0.5em;'>{L['title']} <span style='font-size:1.2em;'>✊✋✌️</span></h1>", unsafe_allow_html=True)

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = {L['win']: 0, L['lose']: 0, L['draw']: 0}
if 'last_result' not in st.session_state:
    st.session_state.last_result = None
if 'last_computer' not in st.session_state:
    st.session_state.last_computer = None
if 'last_player' not in st.session_state:
    st.session_state.last_player = None
if 'history' not in st.session_state:
    st.session_state.history = []

st.markdown(f"<h4 style='text-align:center;'>{L['choose_move']}</h4>", unsafe_allow_html=True)
cols = st.columns(3)
choice = None
with cols[0]:
    if st.button(f"✊\n{L['rock']}", key="rock", help=L['rock'], use_container_width=True):
        choice = "Rock"
with cols[1]:
    if st.button(f"✋\n{L['paper']}", key="paper", help=L['paper'], use_container_width=True):
        choice = "Paper"
with cols[2]:
    if st.button(f"✌️\n{L['scissors']}", key="scissors", help=L['scissors'], use_container_width=True):
        choice = "Scissors"

if choice:
    with st.spinner(L['thinking']):
        import time
        time.sleep(0.6)
    computer = get_computer_choice()
    result = determine_winner(choice, computer)
    st.session_state.last_result = result
    st.session_state.last_computer = computer
    st.session_state.last_player = choice
    # Map result to language
    lang_result = L[result.lower()] if result.lower() in L else result
    # For score dict, always use current language keys
    if L['win'] not in st.session_state.score:
        st.session_state.score = {L['win']: 0, L['lose']: 0, L['draw']: 0}
    st.session_state.score[lang_result] += 1
    st.session_state.history.append({
        "player": L[choice.lower()] if choice.lower() in L else choice,
        "computer": L[computer.lower()] if computer.lower() in L else computer,
        "result": lang_result
    })
    if len(st.session_state.history) > 7:
        st.session_state.history.pop(0)
    store_result(choice, computer, result)
    # Animation feedback
    if result == "Win":
        st.balloons()
    elif result == "Draw":
        st.snow()

if st.session_state.last_result:
    player_disp = L[st.session_state.last_player.lower()] if st.session_state.last_player and st.session_state.last_player.lower() in L else st.session_state.last_player
    computer_disp = L[st.session_state.last_computer.lower()] if st.session_state.last_computer and st.session_state.last_computer.lower() in L else st.session_state.last_computer
    result_disp = L[st.session_state.last_result.lower()] if st.session_state.last_result and st.session_state.last_result.lower() in L else st.session_state.last_result
    st.markdown(f"""
    <div class='result-box'>
        {L['you']} {L['choose_move'][:-1]} <b>{player_disp}</b> <br>
        {L['computer']} {L['choose_move'][:-1]} <b>{computer_disp}</b><br>
        <span style='font-size:1.3em;'>{L['result']}: <b>{result_disp}</b></span>
    </div>
    """, unsafe_allow_html=True)

# Scoreboard
score = st.session_state.score
st.markdown(f"""
<div style='text-align:center; font-size:1.1em; margin-bottom:1em;'>
    <b>{L['score']}</b> — 
    <span style='color:#ffe066;'>{L['wins']}: {score.get(L['win'], 0)}</span> &nbsp; 
    <span style='color:#ff7675;'>{L['losses']}: {score.get(L['lose'], 0)}</span> &nbsp; 
    <span style='color:#74b9ff;'>{L['draws']}: {score.get(L['draw'], 0)}</span>
</div>
""", unsafe_allow_html=True)

# Game history
if st.session_state.history:
    st.markdown(f"<b>{L['recent_games']}</b>", unsafe_allow_html=True)
    for entry in st.session_state.history:
        st.markdown(f"<div class='history-entry'>{L['you']}: {entry['player']}, {L['computer']}: {entry['computer']} — <b>{entry['result']}</b></div>", unsafe_allow_html=True)

reset = st.container().button(L['reset'], key="reset_score", help=L['reset'], use_container_width=True)
if reset:
    st.session_state.score = {L['win']: 0, L['lose']: 0, L['draw']: 0}
    st.session_state.last_result = None
    st.session_state.last_computer = None
    st.session_state.last_player = None
    st.session_state.history = []

# Add a class to the reset button for custom color
st.markdown("""
    <script>
    const btns = window.parent.document.querySelectorAll('button[kind=\"secondary\"]');
    btns.forEach(btn => btn.parentElement.classList.add('reset-btn'));
    </script>
""", unsafe_allow_html=True)

if reset:
    st.session_state.score = {"Win": 0, "Lose": 0, "Draw": 0}
    st.session_state.last_result = None
    st.session_state.last_computer = None
    st.session_state.last_player = None
# After reset, do not show previous round info
if not st.session_state.get('score'):
    st.session_state.score = {"Win": 0, "Lose": 0, "Draw": 0}
