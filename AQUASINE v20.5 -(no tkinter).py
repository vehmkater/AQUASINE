import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide", page_icon="◈")

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    .title { font-size: 2rem; font-weight: bold; letter-spacing: 5px; color: #00ffcc; margin-bottom: 0px; }
    .tagline { color: #222; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 30px; }
    
    /* Textfelder */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        border-radius: 0px !important;
    }
    
    /* Pink Output */
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        border: 1px solid #300 !important;
    }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        height: 3.5rem;
        border-radius: 0px !important;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }

    /* Inputs */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ffcc !important;
        border: 1px solid #111 !important;
        text-align: center;
    }
    .stCodeBlock { border: 1px solid #111 !important; background-color: #050505 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE ---
def glitch_engine(content, seed_val, mode):
    if not content: return ""
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    res = ""
    for i, char in enumerate(content):
        if char in (" ", "\n"):
            res += char
            continue
        char_rng = random.Random(seed_val + i)
        shift = char_rng.randint(1, 1000)
        if mode == "ENCRYPT":
            new_code = GLYPH_BASE + (ord(char) + shift) % RANGE_SIZE
            res += chr(new_code)
        else:
            glyph_code = ord(char)
            orig_code = (glyph_code - GLYPH_BASE - shift) % RANGE_SIZE
            res += chr(orig_code % 256)
    return res

# --- CALLBACKS (Stabilitäts-Kern) ---
def run_encrypt():
    st.session_state.out_data = glitch_engine(st.session_state.in_buffer, st.session_state.s_val, "ENCRYPT")

def run_decrypt():
    st.session_state.out_data = glitch_engine(st.session_state.in_buffer, st.session_state.s_val, "DECRYPT")

def randomize_seed():
    st.session_state.s_val = random.randint(10000, 99999)

# --- STATE ---
if 's_val' not in st.session_state: st.session_state.s_val = 45739
if 'out_data' not in st.session_state: st.session_state.out_data = ""

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    st.text_area("IN", height=200, label_visibility="collapsed", key="in_buffer")
    
    st.markdown("### ◈ SEED")
    c_s1, c_s2 = st.columns([4, 1])
    with c_s1:
        # Der Seed wird direkt im State synchronisiert
        st.text_input("S", key="s_val", label_visibility="collapsed")
    with c_s2:
        st.button("⌬", on_click=randomize_seed)

    st.code(f"{st.session_state.s_val}", language=None)

    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.button("◈ ENCRYPT", on_click=run_encrypt)
    with btn_col2:
        st.button("◈ DECRYPT", on_click=run_decrypt)

with col2:
    st.markdown("### ◈ OUTPUT")
    st.text_area(
        "OUT", 
        value=st.session_state.out_data, 
        height=450, 
        label_visibility="collapsed",
        key="out_display"
    )

st.markdown("---")
st.caption(f"STATUS: ONLINE | DESIGN: vehmkater")
