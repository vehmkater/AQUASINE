import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE ENGINE", layout="wide", page_icon="◈")

# --- CSS (CLEAN & MOBILE OPTIMIZED) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    
    /* Neuer Cleaner Titel */
    .engine-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: bold;
        letter-spacing: 7px;
        text-shadow: 0 0 15px #00ffcc;
        color: #00ffcc;
        margin-bottom: 5px;
        padding-top: 10px;
    }
    
    .tagline { 
        text-align: center;
        color: #444; 
        font-size: 0.7rem; 
        letter-spacing: 5px; 
        margin-bottom: 30px;
        text-transform: uppercase;
    }

    /* Buttons */
    .stButton>button { 
        width: 100% !important; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #222 !important;
        height: 3.5rem;
        border-radius: 0px !important;
        font-weight: bold;
        letter-spacing: 2px;
    }
    .stButton>button:hover { 
        border-color: #ff0055 !important; 
        color: #ff0055 !important; 
        box-shadow: 0 0 15px #ff0055; 
    }

    /* Output Box */
    .stCodeBlock { border: 1px solid #300 !important; background-color: #050505 !important; }
    .stCodeBlock code { color: #ff0055 !important; font-size: 1.1rem !important; }

    /* Inputs */
    .stTextArea textarea { background-color: #050505 !important; color: #00ffcc !important; border: 1px solid #111 !important; border-radius: 0px !important; }
    .stTextInput input { background-color: #000 !important; color: #00ffcc !important; border: 1px solid #111 !important; text-align: center; border-radius: 0px !important; }
    
    /* Mobile Spacing */
    @media (max-width: 800px) {
        .engine-title { font-size: 1.6rem; letter-spacing: 3px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="engine-title">◈ AQUASINE ENGINE</div>', unsafe_allow_html=True)
st.markdown('<p class="tagline">BY VEHMKATER</p>', unsafe_allow_html=True)

# --- ENGINE LOGIC ---
def glitch_engine(content, seed_val):
    if not content: return "", "..."
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
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

# --- STATE ---
if 's_val' not in st.session_state: st.session_state.s_val = 45739
if 'out_cache' not in st.session_state: st.session_state.out_cache = ""
if 'mode_cache' not in st.session_state: st.session_state.mode_cache = "..."

# --- UI LAYOUT ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### ◈ INPUT")
    st.text_area("IN", height=200, label_visibility="collapsed", key="input_buffer")
    
    st.markdown("### ◈ SEED")
    c_s1, c_s2 = st.columns([4, 1])
    with c_s1:
        s_raw = st.text_input("S", value=str(st.session_state.s_val), label_visibility="collapsed")
        try: st.session_state.s_val = int(''.join(filter(str.isdigit, s_raw)) or 0)
        except: pass
    with c_s2:
        if st.button("⌬"):
            st.session_state.s_val = random.randint(10000, 99999)
            st.rerun()
            
    st.code(f" {st.session_state.s_val}", language=None)

    if st.button("◈ EXECUTE TRANSMISSION ◈"):
        res, m = glitch_engine(st.session_state.input_buffer, st.session_state.s_val)
        st.session_state.out_cache = res
        st.session_state.mode_cache = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode_cache}]")
    if st.session_state.out_cache:
        st.code(st.session_state.out_cache, language=None)
    else:
        st.markdown('<div style="border:1px solid #111; padding:50px; color:#222; text-align:center;">AWAITING_UPLINK...</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(f"AQUASINE ENGINE | AUTH: VEHMKATER | BUILD_20.5_STABLE")
