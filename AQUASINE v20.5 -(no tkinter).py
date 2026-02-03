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
    if not content or content.strip() == "": return "EMPTY_DATA_STREAM", "..."
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    
    # Auto-Erkennung (Glyphen-Check)
    is_decrypt = any(GLYPH_BASE <= ord(c) < (GLYPH_BASE + RANGE_SIZE + 800) for c in content[:10])
    
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
    return res, ("DECRYPT" if is_decrypt else "ENCRYPT")

# --- INITIAL STATE ---
if 'seed' not in st.session_state: st.session_state.seed = 45739
if 'out_text' not in st.session_state: st.session_state.out_text = ""
if 'current_mode' not in st.session_state: st.session_state.current_mode = "..."

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    # Wir speichern den Input SOFORT bei jeder Änderung im Session State
    in_text = st.text_area("IN", height=200, label_visibility="collapsed", key="active_input")
    
    st.markdown("### ◈ SEED")
    s_raw = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
    if s_raw:
        try: st.session_state.seed = int(''.join(filter(str.isdigit, s_raw)))
        except: pass

    st.code(f"{st.session_state.seed}", language=None)

    if st.button("⌬ RANDOMIZE"):
        st.session_state.seed = random.randint(10000, 99999)
        st.rerun()

    # EXECUTE Button
    if st.button("◈ EXECUTE ◈"):
        # Wir holen die Daten direkt aus dem "active_input" State
        data_to_process = st.session_state.active_input
        result, mode = glitch_engine(data_to_process, st.session_state.seed)
        st.session_state.out_text = result
        st.session_state.current_mode = mode

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.current_mode}]")
    # Falls das Textfeld leer bleibt, ist hier das Ergebnis direkt im Code-Block (Backup)
    st.text_area(
        "OUT", 
        value=st.session_state.out_text, 
        height=400, 
        label_visibility="collapsed"
    )
    
    if st.session_state.out_text:
        st.caption("RAW_BUFFER_LOG:")
        st.code(st.session_state.out_text, language=None)

st.markdown("---")
st.caption(f"STATUS: ONLINE | DESIGN: vehmkater")
