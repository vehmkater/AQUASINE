import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide", page_icon="◈")

# --- CSS FOR UI ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; }
    
    h1 { margin-bottom: 0px !important; }
    .by-line { font-family: 'Courier', monospace; color: #333; margin-bottom: 25px; font-size: 0.85rem; letter-spacing: 1px; }
    
    /* Text Areas */
    .stTextArea textarea { 
        background-color: #0a0a0a !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
        border: 1px solid #111 !important;
    }
    
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #00ffcc !important;
        font-family: 'Courier', monospace;
        border-radius: 2px;
        text-transform: uppercase;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }
    
    /* Input Fields */
    .stTextInput input {
        background-color: #000 !important;
        color: #ff0055 !important;
        border: 1px solid #222 !important;
        text-align: center;
        font-family: 'Courier', monospace;
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
        
        # Seed wird hier direkt genutzt
        char_rng = random.Random(seed_val + i)
        shift = char_rng.randint(1, 1000)

        if not is_decrypt:
            new_code = GLYPH_BASE + (ord(char) + shift) % RANGE_SIZE
            res += chr(new_code)
        else:
            glyph_code = ord(char)
            orig_code = (glyph_code - GLYPH_BASE - shift) % RANGE_SIZE
            res += chr(orig_code % 256)
            
    return res, "DECRYPTING" if is_decrypt else "ENCRYPTING"

# --- UI STRUCTURE ---
st.title("◈ AQUASINE v20.5")
st.markdown('<div class="by-line">DESIGNED_BY_VEHMKATER</div>', unsafe_allow_html=True)

# Initialize Session State
if 'seed' not in st.session_state:
    st.session_state.seed = 45739

# --- MAIN INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### [ INPUT ]")
    input_text = st.text_area("In", height=250, label_visibility="collapsed", key="input_key")
    
    # Grid Layout for Buttons & Seed
    c1, c2, c3 = st.columns([2, 1, 2])
    
    with c1:
        # Führt den Prozess aus
        execute = st.button("◈ RUN PROCESS ◈")
    
    with c2:
        # Seed Input - Reagiert direkt
        seed_input = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
        try:
            # Update State sofort bei manueller Änderung
            st.session_state.seed = int(''.join(filter(str.isdigit, seed_input)) or 0)
        except:
            pass
            
    with c3:
        # Randomize Button ausgeschrieben
        if st.button("◈ RANDOMIZE SEED ◈"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()

# Processing mit dem aktuellen State-Seed
output_text, mode = glitch_process(input_text, st.session_state.seed)

with col2:
    st.markdown(f"### [ OUTPUT : {mode} ]")
    st.text_area("Out", value=output_text, height=250, label_visibility="collapsed", key="output_field")

st.markdown("---")
st.caption(f"SYSTEM_NODE: ONLINE | ACTIVE_ENTROPY: {st.session_state.seed}")
