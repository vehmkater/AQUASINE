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
    
    /* Pink Output */
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

# --- CORE LOGIC ---
def glitch_process(content, seed_val):
    if not content or content.strip() == "":
        return "", "IDLE"
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    
    # Robuste Erkennung: Wir prüfen die ersten 3 Zeichen
    sample = content.strip()[:3]
    glyph_count = sum(1 for c in sample if GLYPH_BASE <= ord(c) < (GLYPH_BASE + RANGE_SIZE + 1000))
    is_decrypt = glyph_count > 0
    
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
            # Schutz gegen "Out of Range" Fehler
            orig_code = (glyph_code - GLYPH_BASE - shift) % RANGE_SIZE
            res += chr(orig_code % 256)
            
    return res, "DECRYPT" if is_decrypt else "ENCRYPT"

# --- STATE ---
if 'seed' not in st.session_state:
    st.session_state.seed = 45739
if 'output' not in st.session_state:
    st.session_state.output = ""
if 'mode' not in st.session_state:
    st.session_state.mode = "..."

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    in_data = st.text_area("IN", height=200, label_visibility="collapsed", key="input_area")
    
    st.markdown("### ◈ SEED")
    c1, c2 = st.columns([4, 1])
    with c1:
        s_in = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
        try: st.session_state.seed = int(''.join(filter(str.isdigit, s_in)) or 0)
        except: pass
    with c2:
        if st.button("⌬"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()
            
    st.code(f"{st.session_state.seed}", language=None)

    if st.button("◈ EXECUTE ◈"):
        out, m = glitch_process(in_data, st.session_state.seed)
        st.session_state.output = out
        st.session_state.mode = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode}]")
    st.text_area(
        "OUT", 
        value=st.session_state.output, 
        height=385, 
        label_visibility="collapsed",
        key="output_area"
    )

st.markdown("---")
st.caption(f"STATUS: OPERATIONAL | BY: vehmkater")
