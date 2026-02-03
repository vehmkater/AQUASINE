import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide", page_icon="◈")

# --- CSS FOR COMPACT UI ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    h1 { margin-bottom: 0px !important; }
    .by-line { font-family: 'Courier', monospace; color: #333; margin-bottom: 25px; font-size: 0.85rem; letter-spacing: 1px; }
    
    /* Force Word Wrap */
    div[data-testid="stCodeBlock"] pre {
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }
    
    /* Code Blöcke (Seed & Output) */
    .stCodeBlock { 
        border: 1px solid #ff0055 !important; 
        background-color: #0a0a0a !important; 
    }
    
    /* Buttons Styling */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #00ffcc !important;
        font-family: 'Courier', monospace;
        height: 3.5em;
        text-transform: uppercase;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }

    /* Seed Input */
    .stTextInput input {
        background-color: #000 !important;
        color: #ff0055 !important;
        border: 1px solid #222 !important;
        text-align: center;
        font-family: 'Courier', monospace;
        height: 3.5em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def glitch_process(content, seed_val):
    if not content or content.strip() == "":
        return "", "IDLE"
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    first_char = content.strip()[0]
    is_decrypt = GLYPH_BASE <= ord(first_char) < (GLYPH_BASE + RANGE_SIZE + 500)
    res = ""
    for i, char in enumerate(content):
        if char in (" ", "\n"):
            res += char
            continue
        char_rng = random.Random(seed_val + i)
        shift = char_rng.randint(1, 1000)
        if not is_decrypt:
            res += chr(GLYPH_BASE + (ord(char) + shift) % RANGE_SIZE)
        else:
            res += chr((ord(char) - GLYPH_BASE - shift) % RANGE_SIZE % 256)
    return res, "DECRYPTING" if is_decrypt else "ENCRYPTING"

# --- UI STRUCTURE ---
st.title("◈ AQUASINE v20.5")
st.markdown('<div class="by-line">DESIGNED_BY_VEHMKATER</div>', unsafe_allow_html=True)

if 'active_seed' not in st.session_state:
    st.session_state.active_seed = 45739

col1, col2 = st.columns(2)

with col1:
    st.markdown("### [ INPUT ]")
    user_input = st.text_area("In", height=250, label_visibility="collapsed", key="input_key")
    
    # Die kompakte Button-Zeile
    c1, c2, c3 = st.columns([2, 1, 2])
    
    with c1:
        st.button("◈ RUN PROCESS ◈")
    
    with c2:
        # Editierbares Feld
        s_input = st.text_input("S", value=str(st.session_state.active_seed), label_visibility="collapsed")
        if s_input.isdigit():
            st.session_state.active_seed = int(s_input)
            
    with c3:
        if st.button("◈ RANDOMIZE SEED ◈"):
            st.session_state.active_seed = random.randint(10000, 99999)
            st.rerun()
    
    # Das "Kopier-Feld" für den Seed (direkt unter dem Input, sieht aus wie ein Button)
    st.code(f"SEED: {st.session_state.active_seed}", language=None)

output_text, mode = glitch_process(user_input, st.session_state.active_seed)

with col2:
    st.markdown(f"### [ OUTPUT : {mode} ]")
    if output_text:
        st.code(output_text, language=None)
    else:
        st.info("System operational. Awaiting sequence...")

st.markdown("---")
st.caption(f"NODE: ONLINE | BY: VEHMKATER")
