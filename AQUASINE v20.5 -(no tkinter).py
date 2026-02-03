import streamlit as st
import random

# --- SEITEN-LAYOUT ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide")

# --- CSS FÜR CYBER-LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    .stTextArea textarea { 
        background-color: #0a0a0a !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
        border: 1px solid #222 !important;
    }
    /* Spezialfarbe für den Output-Bereich */
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
    }
    .stButton>button { 
        width: 100%; background-color: #111; color: #00ffcc; border: 1px solid #00ffcc; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- DIE LOGIK ---
def glitch_process(content, seed_val):
    if not content:
        return "", "IDLE"
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    
    # Check ob verschlüsselt oder entschlüsselt (Glyphen-Erkennung)
    is_decrypt = GLYPH_BASE <= ord(content.strip()[0]) < (GLYPH_BASE + RANGE_SIZE + 500)
    
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
            
    return res, "DECRYPTING" if is_decrypt else "ENCRYPTING"

# --- UI STRUKTUR ---
st.title("◈ AQUASINE v20.5 - NODE")

# Sidebar für Seed
with st.sidebar:
    st.markdown("### SYSTEM_CTRL")
    if 'seed' not in st.session_state:
        st.session_state.seed = 42839
    
    seed_input = st.text_input("ENTROPY_SEED", value=str(st.session_state.seed))
    
    if st.button("RANDOMIZE SEED"):
        st.session_state.seed = random.randint(10000, 99999)
        st.rerun()

    try:
        current_seed = int(''.join(filter(str.isdigit, seed_input)) or 0)
    except:
        current_seed = 0

# Haupt-Interface
col1, col2 = st.columns(2)

with col1:
    st.markdown("### [ INPUT_STREAM ]")
    # Hier tippt der User
    input_text = st.text_area("In", height=400, label_visibility="collapsed", key="in")

# Logik wird HIER ausgeführt (zwischen den Spalten)
output_text, mode = glitch_process(input_text, current_seed)

with col2:
    st.markdown(f"### [ OUTPUT_STREAM : {mode} ]")
    # Hier wird das Ergebnis SOFORT angezeigt
    st.text_area("Out", value=output_text, height=400, label_visibility="collapsed", key="out")

st.markdown("---")
st.caption(f"AQUASINE CORE ACTIVE | SEED: {current_seed}")
