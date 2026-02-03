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
        font-weight: bold;
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

# --- CORE ENGINE ---
def glitch_engine(content, seed_val):
    if not content: return "", "..."
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    # Auto-Erkennung: Prüfe die ersten Zeichen auf Glyphen
    is_decrypt = any(GLYPH_BASE <= ord(c) < (GLYPH_BASE + RANGE_SIZE + 500) for c in content[:10])
    
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

# --- STATE MANAGEMENT ---
if 's_val' not in st.session_state: st.session_state.s_val = 45739
if 'out_cache' not in st.session_state: st.session_state.out_cache = ""
if 'mode_cache' not in st.session_state: st.session_state.mode_cache = "..."

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    # Der Key "input_buffer" ist entscheidend - er speichert den Text permanent
    st.text_area("IN", height=200, label_visibility="collapsed", key="input_buffer")
    
    st.markdown("### ◈ SEED")
    c1, c2 = st.columns([4, 1])
    with c1:
        s_raw = st.text_input("S", value=str(st.session_state.s_val), label_visibility="collapsed")
        try: st.session_state.s_val = int(''.join(filter(str.isdigit, s_raw)) or 0)
        except: pass
    with c2:
        if st.button("⌬"):
            st.session_state.s_val = random.randint(10000, 99999)
            st.rerun()
            
    st.code(f"{st.session_state.s_val}", language=None)

    # EIN BUTTON VERSION
    if st.button("◈ EXECUTE ◈"):
        # Wir holen den Text direkt aus dem permanenten Speicher "input_buffer"
        raw_text = st.session_state.input_buffer
        res, m = glitch_engine(raw_text, st.session_state.s_val)
        st.session_state.out_cache = res
        st.session_state.mode_cache = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode_cache}]")
    st.text_area(
        "OUT", 
        value=st.session_state.out_cache, 
        height=450, 
        label_visibility="collapsed"
    )

st.markdown("---")
st.caption(f"STATUS: OPERATIONAL | BY: vehmkater")
