import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE ENGINE", layout="wide", page_icon="◈")

# --- CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    
    /* ASCII Header Styling */
    .ascii-header { 
        font-family: 'Courier New', monospace; 
        white-space: pre; 
        color: #00ffcc; 
        line-height: 1.2; 
        font-weight: bold;
        text-shadow: 0 0 10px #00ffcc;
        margin-bottom: 20px;
    }
    
    .tagline { color: #222; font-size: 0.8rem; letter-spacing: 5px; margin-bottom: 30px; }
    
    /* Input Bereich */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        border-radius: 0px !important;
    }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        height: 4rem;
        border-radius: 0px !important;
        letter-spacing: 3px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        border-color: #ff0055 !important; 
        color: #ff0055 !important;
        box-shadow: 0 0 15px #ff0055;
    }

    /* Seed Input */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ffcc !important;
        border: 1px solid #111 !important;
        text-align: center;
    }

    /* Das Output Fenster (Code-Block) */
    .stCodeBlock { 
        border: 1px solid #300 !important; 
        background-color: #050505 !important; 
    }
    .stCodeBlock code {
        color: #ff0055 !important;
        font-size: 1.1rem !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #111; }
    ::-webkit-scrollbar-thumb:hover { background: #ff0055; }
    </style>
    """, unsafe_allow_html=True)

# --- ASCII ART HEADER ---
ascii_banner = """
 █████╗  ██████╗ ██╗   ██╗ █████╗ ███████╗██╗███╗   ██╗███████╗
██╔══██╗██╔═══██╗██║   ██║██╔══██╗██╔════╝██║████╗  ██║██╔════╝
███████║██║   ██║██║   ██║███████║███████╗██║██╔██╗ ██║█████╗  
██╔══██║██║▄▄ ██║██║   ██║██╔══██║╚════██║██║██║╚██╗██║██╔══╝  
██║  ██║╚██████╔╝╚██████╔╝██║  ██║███████║██║██║ ╚████║███████╗
╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝ ENGINE
"""
st.markdown(f'<div class="ascii-header">{ascii_banner}</div>', unsafe_allow_html=True)
st.markdown('<p class="tagline">DESIGNED BY VEHMKATER</p>', unsafe_allow_html=True)

# --- ENGINE ---
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
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ◈ DATA_INPUT")
    st.text_area("IN", height=200, label_visibility="collapsed", key="input_buffer")
    
    st.markdown("### ◈ CORE_SEED")
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

    if st.button("◈ EXECUTE_TRANSMISSION ◈"):
        raw_text = st.session_state.input_buffer
        res, m = glitch_engine(raw_text, st.session_state.s_val)
        st.session_state.out_cache = res
        st.session_state.mode_cache = m

with col2:
    st.markdown(f"### ◈ OUTPUT_STREAM [{st.session_state.mode_cache}]")
    
    # Das Output-Fenster mit integriertem Copy-Button
    if st.session_state.out_cache:
        st.code(st.session_state.out_cache, language=None)
    else:
        st.markdown("""
        <div style="border: 1px solid #111; padding: 20px; color: #222; text-align: center;">
        SYSTEM_IDLE: AWAITING_INPUT...
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"AQUASINE_ENGINE | VERSION_20.5 | AUTH: VEHMKATER | NODE_ONLINE")
