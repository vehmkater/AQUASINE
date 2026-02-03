import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide", page_icon="◈")

# --- ADVANCED CYBER CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@100;400&display=swap');

    .stApp { background-color: #000000; color: #00ffcc; font-family: 'JetBrains Mono', monospace; }
    
    /* Header & Tag */
    .main-title { font-size: 1.8rem; letter-spacing: 5px; font-weight: 100; color: #00ffcc; margin-bottom: 0px; }
    .vehm-tag { font-size: 0.7rem; color: #222; letter-spacing: 3px; margin-bottom: 30px; }

    /* Input & Output Fields */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        border-radius: 0px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
    }
    
    /* Mobile Word-Wrap Fix & Pink Output */
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        border: 1px solid #1a000a !important;
    }
    
    /* Minimalist Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        border-radius: 0px !important;
        height: 3.5rem;
        letter-spacing: 4px;
        transition: 0.3s;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; background-color: #0a0005 !important; }

    /* Seed Input Field */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ffcc !important;
        border: 1px solid #111 !important;
        text-align: center;
        border-radius: 0px !important;
        letter-spacing: 2px;
    }

    /* Seed Copy Box */
    .stCodeBlock { background-color: #050505 !important; border: 1px solid #111 !important; border-radius: 0px !important; }
    code { color: #00ffcc !important; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def glitch_process(content, seed_val):
    if not content or content.strip() == "":
        return "", "IDLE"
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    
    # Analyze first non-whitespace char for mode detection
    stripped = content.strip()
    first_char = stripped[0]
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
    return res, "DECRYPT" if is_decrypt else "ENCRYPT"

# --- UI STRUCTURE ---
st.markdown('<p class="main-title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="vehm-tag">VEHMKATER_CORE_LINKED</p>', unsafe_allow_html=True)

if 'seed' not in st.session_state:
    st.session_state.seed = 45739

# --- LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 01_DATA_IN")
    input_text = st.text_area("In", height=200, label_visibility="collapsed", key="in_field", placeholder="---")
    
    st.markdown("### 02_ENTROPY")
    # Manual Seed Input
    seed_input_raw = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
    
    # Filter only digits
    seed_digits = ''.join(filter(str.isdigit, seed_input_raw))
    current_seed = int(seed_digits) if seed_digits else 0
    st.session_state.seed = current_seed

    # Display for copying
    st.code(f"{current_seed}", language=None)

    # Action Buttons
    if st.button("RANDOMIZE"):
        st.session_state.seed = random.randint(10000, 99999)
        st.rerun()
        
    execute_trigger = st.button("EXECUTE")

# Calculation (always runs, but button can be used for force-refresh)
output_text, mode = glitch_process(input_text, current_seed)

with col2:
    st.markdown(f"### 03_DATA_OUT [{mode}]")
    # THE FIX: We use a key that doesn't conflict and ensure the value is explicitly passed
    st.text_area(
        "Out", 
        value=output_text, 
        height=380, 
        label_visibility="collapsed", 
        key="out_field"
    )

st.markdown("---")
st.caption(f"NODE_STATUS: ONLINE | STABILITY: 100% | CORE: {current_seed}")
