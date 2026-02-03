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
    
    /* Glitch-Red Code Block (Output) */
    .stCodeBlock { 
        border: 1px solid #ff0055 !important; 
        background-color: #050505 !important;
    }
    .stCodeBlock code {
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
        height: 3em;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }
    
    /* Seed Input */
    .stTextInput input {
        background-color: #000 !important;
        color: #ff0055 !important;
        border: 1px solid #222 !important;
        text-align: center;
        font-family: 'Courier', monospace;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def glitch_process(content, seed_val):
    if not content or content.strip() == "":
        return "", "IDLE"
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    stripped = content.strip()
    first_char = stripped[0]
    
    # Detection logic
    is_decrypt = GLYPH_BASE <= ord(first_char) < (GLYPH_BASE + RANGE_SIZE + 500)
    
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
            
    return res, "DECRYPTING" if is_decrypt else "ENCRYPTING"

# --- UI STRUCTURE ---
st.title("◈ AQUASINE v20.5")
st.markdown('<div class="by-line">DESIGNED_BY_VEHMKATER</div>', unsafe_allow_html=True)

# Persistent Seed State
if 'seed' not in st.session_state:
    st.session_state.seed = 45739

# --- MAIN INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### [ INPUT ]")
    # key="input_key" sorgt dafür, dass die Eingabe erhalten bleibt
    user_input = st.text_area("In", height=250, label_visibility="collapsed", key="input_key")
    
    c1, c2, c3 = st.columns([2, 1, 2])
    
    with c1:
        # Trigger
        run_btn = st.button("◈ RUN PROCESS ◈")
    
    with c2:
        # Manuelle Seed-Eingabe
        s_input = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed", key="s_field")
        try:
            st.session_state.seed = int(''.join(filter(str.isdigit, s_input)) or 0)
        except:
            pass
            
    with c3:
        # Randomize
        if st.button("◈ RANDOMIZE SEED ◈"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()

# Berechnung wird immer ausgeführt, wenn Text vorhanden ist
output_text, mode = glitch_process(user_input, st.session_state.seed)

with col2:
    st.markdown(f"### [ OUTPUT : {mode} ]")
    if output_text:
        # st.code bietet den besten "Copy-Button" für Handys
        st.code(output_text, language=None)
    else:
        st.info("Awaiting input sequence...")

st.markdown("---")
st.caption(f"NODE: OPERATIONAL | SEED: {st.session_state.seed}")
