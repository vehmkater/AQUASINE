import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE ENGINE", layout="wide", page_icon="◈")

# --- CSS (RESPONSIVE OPTIMIZED) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    
    /* Responsive ASCII / Header */
    .header-container {
        text-align: center;
        padding: 10px;
    }
    
    .mobile-title {
        font-size: 1.8rem;
        font-weight: bold;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #00ffcc;
        margin: 0;
    }

    .ascii-banner { 
        font-family: 'Courier New', monospace; 
        white-space: pre; 
        color: #00ffcc; 
        line-height: 1; 
        font-size: 0.6vw; /* Skaliert mit der Breite */
        display: block;
    }
    
    /* Verstecke ASCII auf sehr kleinen Handys, zeige Text-Titel */
    @media (max-width: 600px) {
        .ascii-banner { display: none; }
        .mobile-title { display: block; font-size: 1.5rem; }
    }

    .tagline { color: #333; font-size: 0.7rem; letter-spacing: 3px; margin-bottom: 20px; }
    
    /* Buttons & Inputs */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        height: 3.5rem;
        border-radius: 0px !important;
        letter-spacing: 2px;
    }
    
    /* Code/Output Box */
    .stCodeBlock { 
        border: 1px solid #300 !important; 
        background-color: #050505 !important; 
    }
    .stCodeBlock code { color: #ff0055 !important; }

    /* Fix für Mobile Padding */
    .block-container { padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header-container">
        <div class="ascii-banner">
 █████╗  ██████╗ ██╗   ██╗ █████╗ ███████╗██╗███╗   ██╗███████╗
██╔══██╗██╔═══██╗██║   ██║██╔══██╗██╔════╝██║████╗  ██║██╔════╝
███████║██║   ██║██║   ██║███████║███████╗██║██╔██╗ ██║█████╗  
██╔══██║██║▄▄ ██║██║   ██║██╔══██║╚════██║██║██║╚██╗██║██╔══╝  
██║  ██║╚██████╔╝╚██████╔╝██║  ██║███████║██║██║ ╚████║███████╗
╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝ ENGINE
        </div>
        <div class="mobile-title">◈ AQUASINE ENGINE</div>
        <p class="tagline">BY VEHMKATER</p>
    </div>
    """, unsafe_allow_html=True)

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
# Auf dem Handy werden diese Spalten automatisch untereinander angezeigt
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ◈ INPUT")
    st.text_area("IN", height=150, label_visibility="collapsed", key="input_buffer")
    
    c1, c2 = st.columns([3, 1])
    with c1:
        s_raw = st.text_input("SEED", value=str(st.session_state.s_val), label_visibility="collapsed")
        try: st.session_state.s_val = int(''.join(filter(str.isdigit, s_raw)) or 0)
        except: pass
    with c2:
        if st.button("⌬"):
            st.session_state.s_val = random.randint(10000, 99999)
            st.rerun()
            
    st.code(f"S: {st.session_state.s_val}", language=None)

    if st.button("◈ EXECUTE ◈"):
        res, m = glitch_engine(st.session_state.input_buffer, st.session_state.s_val)
        st.session_state.out_cache = res
        st.session_state.mode_cache = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode_cache}]")
    if st.session_state.out_cache:
        st.code(st.session_state.out_cache, language=None)
    else:
        st.markdown('<div style="color:#222; text-align:center; padding:20px; border:1px solid #111;">AWAITING...</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption(f"AQUASINE | AUTH: VEHMKATER")
