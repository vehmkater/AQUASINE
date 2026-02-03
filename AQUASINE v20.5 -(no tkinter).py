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
    
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        border-radius: 0px !important;
    }
    
    /* Pink Output Styling */
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        border: 1px solid #300 !important;
    }
    
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        height: 3.5rem;
        border-radius: 0px !important;
        letter-spacing: 1px;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }

    .stTextInput input {
        background-color: #000 !important;
        color: #00ffcc !important;
        border: 1px solid #111 !important;
        text-align: center;
        border-radius: 0px !important;
    }
    .stCodeBlock { border: 1px solid #111 !important; background-color: #050505 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
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
        else: # DECRYPT
            glyph_code = ord(char)
            orig_code = (glyph_code - GLYPH_BASE - shift) % RANGE_SIZE
            res += chr(orig_code % 256)
    return res

# --- STATE ---
if 's_val' not in st.session_state: st.session_state.s_val = 45739
if 'out_data' not in st.session_state: st.session_state.out_data = ""

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    # Buffer Key für Stabilität
    in_text = st.text_area("IN", height=200, label_visibility="collapsed", key="input_buffer")
    
    st.markdown("### ◈ SEED")
    c_s1, c_s2 = st.columns([4, 1])
    with c_s1:
        s_input = st.text_input("S", value=str(st.session_state.s_val), label_visibility="collapsed")
        try: st.session_state.s_val = int(''.join(filter(str.isdigit, s_input)) or 0)
        except: pass
    with c_s2:
        if st.button("⌬"):
            st.session_state.s_val = random.randint(10000, 99999)
            st.rerun()

    # Seed Copy Display
    st.code(f"{st.session_state.s_val}", language=None)

    # Die zwei Aktions-Buttons nebeneinander
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("◈ ENCRYPT"):
            st.session_state.out_data = glitch_engine(st.session_state.input_buffer, st.session_state.s_val, "ENCRYPT")
    with btn_col2:
        if st.button("◈ DECRYPT"):
            st.session_state.out_data = glitch_engine(st.session_state.input_buffer, st.session_state.s_val, "DECRYPT")

with col2:
    st.markdown("### ◈ OUTPUT")
    st.text_area(
        "OUT", 
        value=st.session_state.out_data, 
        height=450, 
        label_visibility="collapsed",
        key="final_output_field"
    )

st.markdown("---")
st.caption(f"STATUS: ONLINE | NODE: 01 | BY: vehmkater")
