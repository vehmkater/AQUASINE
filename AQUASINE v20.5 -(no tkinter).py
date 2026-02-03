import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide", page_icon="◈")

# --- CYBER DESIGN CSS ---
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
    
    /* Output Bereich (Pink) */
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        border: 1px solid #300 !important;
    }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #222 !important;
        height: 3.5rem;
        border-radius: 0px !important;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }

    /* Seed Input */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ffcc !important;
        border: 1px solid #111 !important;
        text-align: center;
        border-radius: 0px !important;
    }
    
    /* Seed Copy Box */
    .stCodeBlock { border: 1px solid #111 !important; background-color: #050505 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def glitch_process(content, seed_val):
    if not content or content.strip() == "":
        return "", "..."
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    stripped = content.strip()
    is_decrypt = GLYPH_BASE <= ord(stripped[0]) < (GLYPH_BASE + RANGE_SIZE + 500)
    
    res = ""
    for i, char in enumerate(content):
        if char in (" ", "\n"):
            res += char
            continue
        char_rng = random.Random(seed_val + i)
        shift = char_rng.randint(1, 1000)
        if not is_decrypt:
            new_code = GLYPH_BASE + (ord(char) + shift) % RANGE_SIZE
            res += chr(new_code)
        else:
            glyph_code = ord(char)
            orig_code = (glyph_code - GLYPH_BASE - shift) % RANGE_SIZE
            res += chr(orig_code % 256)
    return res, "DECRYPT" if is_decrypt else "ENCRYPT"

# --- SESSION STATE INITIALISIERUNG ---
if 'seed' not in st.session_state:
    st.session_state.seed = 45739
if 'output_cache' not in st.session_state:
    st.session_state.output_cache = ""
if 'mode_cache' not in st.session_state:
    st.session_state.mode_cache = "..."

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    user_input = st.text_area("In", height=200, label_visibility="collapsed", key="in_field")
    
    st.markdown("### ◈ SEED")
    s_col1, s_col2 = st.columns([4, 1])
    with s_col1:
        seed_raw = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
        try:
            st.session_state.seed = int(''.join(filter(str.isdigit, seed_raw)) or 0)
        except: pass
    with s_col2:
        if st.button("⌬"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()

    # Seed Copy Display (Wieder da!)
    st.code(f"{st.session_state.seed}", language=None)

    if st.button("◈ EXECUTE ◈"):
        out, m = glitch_process(user_input, st.session_state.seed)
        st.session_state.output_cache = out
        st.session_state.mode_cache = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode_cache}]")
    # Das Textfeld nutzt jetzt den Cache, damit der Output stabil bleibt
    st.text_area(
        "Out", 
        value=st.session_state.output_cache, 
        height=350, 
        label_visibility="collapsed", 
        key="out_field"
    )

st.markdown("---")
st.caption(f"STATUS: OPERATIONAL | BY: vehmkater")
