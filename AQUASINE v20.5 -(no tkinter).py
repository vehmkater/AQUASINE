import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide", page_icon="◈")

# --- CSS FOR MINIMALIST CYBER LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    section[data-testid="stSidebar"] { display: none; } /* Sidebar komplett ausblenden */
    
    .by-line { font-family: 'Courier', monospace; color: #222; margin-bottom: 25px; font-size: 0.8rem; letter-spacing: 2px; }
    
    /* Text Areas */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
        border: 1px solid #111 !important;
        border-radius: 0px;
    }
    
    /* Output Area (Pink) */
    div[data-testid="column"]:nth-child(2) textarea {
        color: #ff0055 !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        border: 1px solid #200 !important;
    }
    
    /* Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #000 !important; 
        color: #00ffcc !important; 
        border: 1px solid #111 !important;
        font-family: 'Courier', monospace;
        border-radius: 0px;
        margin-top: 5px;
        letter-spacing: 2px;
    }
    .stButton>button:hover { border-color: #ff0055 !important; color: #ff0055 !important; }
    
    /* Input Fields */
    .stTextInput input {
        background-color: #000 !important;
        color: #00ffcc !important;
        border: 1px solid #111 !important;
        text-align: center;
        font-family: 'Courier', monospace;
        border-radius: 0px;
    }

    /* Code Block als schlichtes Display */
    .stCodeBlock {
        background-color: #050505 !important;
        border: 1px solid #111 !important;
    }
    code { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def glitch_process(content, seed_val):
    if not content or content.strip() == "":
        return "", "..."
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    
    first_char = content.strip()[0]
    is_decrypt = GLYPH_BASE <= ord(first_char) < (GLYPH_BASE + RANGE_SIZE + 500)
    
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

# --- UI STRUCTURE ---
st.title("◈ AQUASINE v20.5")
st.markdown('<div class="by-line">VEHMKATER_CORE_LINKED</div>', unsafe_allow_html=True)

if 'seed' not in st.session_state:
    st.session_state.seed = 45739

# --- MAIN INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 01_INPUT")
    input_text = st.text_area("In", height=200, label_visibility="collapsed", key="input_key", placeholder="---")
    
    # Minimalist Seed Section
    st.markdown("### 02_SEED")
    # Einfaches Eingabefeld ohne Label
    seed_val_str = st.text_input("S", value=str(st.session_state.seed), label_visibility="collapsed")
    
    try:
        current_seed = int(''.join(filter(str.isdigit, seed_val_str)) or 0)
        st.session_state.seed = current_seed
    except: current_seed = st.session_state.seed

    # Schlichte Anzeige des aktuellen Seeds zum Kopieren
    st.code(f"{current_seed}", language=None)

    # Buttons
    if st.button("RANDOMIZE"):
        st.session_state.seed = random.randint(10000, 99999)
        st.rerun()
        
    execute = st.button("EXECUTE")

output_text, mode = glitch_process(input_text, current_seed)

with col2:
    st.markdown(f"### 03_OUTPUT [{mode}]")
    st.text_area(
        "Out", 
        value=output_text, 
        height=350, 
        label_visibility="collapsed", 
        key="output_field"
    )

st.markdown("---")
st.caption(f"NODE: ONLINE | STATUS: OPERATIONAL")
