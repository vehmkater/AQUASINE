import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide", page_icon="◈")

# --- CYBER DESIGN CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    
    /* Headers */
    .title { font-size: 2.2rem; font-weight: bold; letter-spacing: 5px; color: #00ffcc; margin-bottom: 0px; }
    .tagline { color: #222; font-size: 0.8rem; letter-spacing: 2px; margin-bottom: 30px; }

    /* Input Fields */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        font-size: 1rem !important;
        border-radius: 0px !important;
    }
    
    /* Output Field (Pink) */
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        border: 1px solid #300 !important;
    }
    
    /* Cyber Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #222 !important;
        height: 3rem;
        border-radius: 0px !important;
        letter-spacing: 2px;
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

    /* Seed Copy Block */
    .stCodeBlock { background-color: #050505 !important; border: 1px solid #111 !important; }
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

# --- SESSION INITIALIZATION ---
if 'seed' not in st.session_state:
    st.session_state.seed = 45739
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""
if 'mode' not in st.session_state:
    st.session_state.mode = "..."

# --- UI STRUCTURE ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">DESIGNED_BY_VEHMKATER</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    input_text = st.text_area("In", height=200, label_visibility="collapsed", key="main_in", placeholder="---")
    
    # Seed Control Row
    st.markdown("### ◈ SEED")
    s_col1, s_col2 = st.columns([4, 1])
    with s_col1:
        seed_in = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
        try:
            current_seed = int(''.join(filter(str.isdigit, seed_in)) or 0)
            st.session_state.seed = current_seed
        except: current_seed = st.session_state.seed
    with s_col2:
        # Glyphe statt Emoji
        if st.button("⌬"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()

    # Seed Copy Display
    st.code(f"{st.session_state.seed}", language=None)

    # Execution Trigger
    if st.button("◈ EXECUTE ◈"):
        out, m = glitch_process(input_text, st.session_state.seed)
        st.session_state.output_text = out
        st.session_state.mode = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode}]")
    st.text_area(
        "Out", 
        value=st.session_state.output_text, 
        height=380, 
        label_visibility="collapsed", 
        key="main_out"
    )

st.markdown("---")
st.caption(f"NODE: OPERATIONAL | BY: VEHMKATER | ID: {st.session_state.seed}")
