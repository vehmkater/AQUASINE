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
    
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        border: 1px solid #300 !important;
    }
    
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        height: 4rem;
        border-radius: 0px !important;
        font-weight: bold;
        letter-spacing: 2px;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }

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
def glitch_engine(content, seed_val):
    if not content: return "", "IDLE"
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    stripped = content.strip()
    
    # Auto-Detection
    is_decrypt = any(GLYPH_BASE <= ord(c) < (GLYPH_BASE + RANGE_SIZE + 500) for c in stripped[:5])
    
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

# --- STATE ---
if 's_val' not in st.session_state: st.session_state.s_val = 45739
if 'out_data' not in st.session_state: st.session_state.out_data = ""
if 'mode_tag' not in st.session_state: st.session_state.mode_tag = "..."

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    # Festes Key-Binding für den Text-Snapshot
    st.text_area("IN", height=200, label_visibility="collapsed", key="main_input_buffer")
    
    st.markdown("### ◈ SEED")
    # Manuelle Seed-Eingabe
    s_raw = st.text_input("S", value=str(st.session_state.s_val), label_visibility="collapsed")
    try: 
        st.session_state.s_val = int(''.join(filter(str.isdigit, s_raw)) or 45739)
    except: pass

    # Seed Copy Fenster (direkt unter dem Input)
    st.code(f"{st.session_state.s_val}", language=None)

    # Random Button (⌬)
    if st.button("⌬ RANDOMIZE"):
        st.session_state.s_val = random.randint(10000, 99999)
        st.rerun()

    # EXECUTE Button
    if st.button("◈ EXECUTE ◈"):
        # Daten direkt aus dem Key-Buffer ziehen
        txt = st.session_state.main_input_buffer
        res, m = glitch_engine(txt, st.session_state.s_val)
        st.session_state.out_data = res
        st.session_state.mode_tag = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode_tag}]")
    st.text_area(
        "OUT", 
        value=st.session_state.out_data, 
        height=475, 
        label_visibility="collapsed",
        key="display_output"
    )

st.markdown("---")
st.caption(f"STATUS: ONLINE | DESIGN: vehmkater")
