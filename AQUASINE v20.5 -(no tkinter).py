import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE ENGINE", layout="wide", page_icon="◈")

# --- CSS (RESPONSIVE & MOBILE OPTIMIZED) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; font-family: 'Courier New', monospace; }
    
    /* Header Container */
    .header-box { text-align: center; padding: 10px; margin-bottom: 20px; }
    
    /* ASCII nur für Desktop (Breite Bildschirme) */
    .ascii-banner { 
        font-family: 'Courier New', monospace; 
        white-space: pre; 
        color: #00ffcc; 
        font-size: 0.7vw; 
        line-height: 1.1;
        display: block;
    }

    /* Titel für Mobile (Kompakt) */
    .mobile-title {
        display: none;
        font-size: 1.8rem;
        font-weight: bold;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #00ffcc;
    }
    
    .tagline { color: #444; font-size: 0.7rem; letter-spacing: 5px; margin-top: 5px; text-transform: uppercase; }

    /* Media Query für Handys */
    @media (max-width: 800px) {
        .ascii-banner { display: none; }
        .mobile-title { display: block; }
    }

    /* Buttons & Inputs Styling */
    .stButton>button { 
        width: 100% !important; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #222 !important;
        height: 3.5rem;
        border-radius: 0px !important;
        font-weight: bold;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; box-shadow: 0 0 10px #ff0055; }

    /* Code/Output Box */
    .stCodeBlock { border: 1px solid #300 !important; background-color: #050505 !important; }
    .stCodeBlock code { color: #ff0055 !important; font-size: 1rem !important; }

    /* Input Styling */
    .stTextArea textarea { background-color: #050505 !important; color: #00ffcc !important; border: 1px solid #111 !important; }
    .stTextInput input { background-color: #000 !important; color: #00ffcc !important; border: 1px solid #111 !important; text-align: center; }
    
    /* Padding Adjustments */
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
    <div class="header-box">
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
# Spalten-Verhältnis optimiert für Desktop, stapelt sich auf Mobile
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### ◈ INPUT")
    st.text_area("IN", height=180, label_visibility="collapsed", key="input_buffer")
    
    st.markdown("### ◈ SEED")
    c_s1, c_s2 = st.columns([4, 1])
    with c_s1:
        s_raw = st.text_input("SEED_VAL", value=str(st.session_state.s_val), label_visibility="collapsed")
        try: st.session_state.s_val = int(''.join(filter(str.isdigit, s_raw)) or 0)
        except: pass
    with c_s2:
        if st.button("⌬"):
            st.session_state.s_val = random.randint(10000, 99999)
            st.rerun()
            
    st.code(f"S: {st.session_state.s_val}", language=None)

    if st.button("◈ EXECUTE TRANSMISSION ◈"):
        res, m = glitch_engine(st.session_state.input_buffer, st.session_state.s_val)
        st.session_state.out_cache = res
        st.session_state.mode_cache = m

with col2:
    st.markdown(f"### ◈ OUTPUT [{st.session_state.mode_cache}]")
    if st.session_state.out_cache:
        st.code(st.session_state.out_cache, language=None)
    else:
        st.markdown("""
        <div style="border: 1px solid #111; padding: 40px; color: #222; text-align: center; font-style: italic;">
        AWAITING_UPLINK...
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"AQUASINE ENGINE | AUTH: VEHMKATER | STABLE_BUILD_20.5")
