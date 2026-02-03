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
    if not content: return "", "..."
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    stripped = content.strip()
    if not stripped: return "", "..."
    
    # Check if first char is a glyph
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

# --- PERSISTENT STATE ---
if 'seed' not in st.session_state: st.session_state.seed = 45739
if 'out_cache' not in st.session_state: st.session_state.out_cache = ""
if 'mode_label' not in st.session_state: st.session_state.mode_label = "..."

# --- UI ---
st.markdown('<p class="title">◈ AQUASINE v20.5</p>', unsafe_allow_html=True)
st.markdown('<p class="tagline">vehmkater</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ INPUT")
    # Der Trick: Wir weisen dem Input einen festen Key zu
    in_data = st.text_area("IN", height=200, label_visibility="collapsed", key="user_input_key")
    
    st.markdown("### ◈ SEED")
    c1, c2 = st.columns([4, 1])
    with c1:
        s_val = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
        try: st.session_state.seed = int(''.join(filter(str.isdigit, s_val)) or 0)
        except: pass
    with c2:
        if st.button("⌬"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()
            
    st.code(f"{st.session_state.seed}", language=None)

    # EXECUTE greift jetzt direkt auf den State des Textfeldes zu
    if st.button("◈ EXECUTE ◈"):
        # WICHTIG: Wir holen die Daten direkt aus dem Key-Speicher
        raw_text = st.session_state.user_input_key
        if raw_text:
            out, m = glitch_process(raw_text, st.session_state.seed)
            st.session_state.out_cache = out
            st.session_state.mode_label = m
        else:
            st.session_state.out_cache = "ERROR: NO_INPUT_DETECTED"

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode_label}]")
    st.text_area(
        "OUT", 
        value=st.session_state.out_cache, 
        height=385, 
        label_visibility="collapsed",
        key="static_output_field"
    )

st.markdown("---")
st.caption(f"STATUS: OPERATIONAL | DESIGN: vehmkater")
