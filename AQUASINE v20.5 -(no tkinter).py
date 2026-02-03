import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide")

# --- CSS FOR CYBER LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; }
    
    /* Input Area */
    .stTextArea textarea { 
        background-color: #0a0a0a !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
        border: 1px solid #222 !important;
    }
    
    /* Stable Output Box */
    .stCodeBlock { 
        border: 1px solid #ff0055 !important; 
        background-color: #050505 !important;
    }
    
    /* Button Styling */
    .stButton>button { 
        width: 100%; 
        background-color: #111 !important; 
        color: #00ffcc !important; 
        border: 1px solid #00ffcc !important;
        font-weight: bold;
        height: 3em;
        font-family: 'Courier', monospace;
    }
    .stButton>button:hover { 
        border-color: #ff0055 !important; 
        color: #ff0055 !important; 
    }
    h3 { font-family: 'Courier', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE LOGIC ---
def glitch_process(content, seed_val):
    if not content or content.strip() == "":
        return "", "IDLE"
    
    GLYPH_BASE = 0x2200
    RANGE_SIZE = 256
    
    # Detection: Is the first character from the glyph block?
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
            # ENCRYPT
            new_code = GLYPH_BASE + (ord(char) + shift) % RANGE_SIZE
            res += chr(new_code)
        else:
            # DECRYPT
            glyph_code = ord(char)
            orig_code = (glyph_code - GLYPH_BASE - shift) % RANGE_SIZE
            res += chr(orig_code % 256)
            
    return res, "DECRYPTING" if is_decrypt else "ENCRYPTING"

# --- UI STRUCTURE ---
st.title("◈ AQUASINE v20.5 - GLITCH HEX")

# Sidebar for Entropy Control
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

# Main Interface Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("### [ INPUT_STREAM ]")
    # Text input field
    input_text = st.text_area("In", height=350, label_visibility="collapsed", key="input_key", placeholder="Waiting for data input...")
    
    # Execution trigger
    execute = st.button("◈ RUN PROCESS ◈")

# Processing logic
output_text = ""
mode = "WAITING"

if execute or input_text:
    output_text, mode = glitch_process(input_text, current_seed)

with col2:
    st.markdown(f"### [ OUTPUT_STREAM : {mode} ]")
    if output_text:
        # Render stable output using st.code
        st.code(output_text, language=None)
        st.caption("Use the icon in the top-right corner of the red box to copy.")
    else:
        st.info("Input data required. Press 'Run Process' to execute.")

st.markdown("---")
st.caption(f"AQUASINE CORE ACTIVE | SEED: {current_seed} | NODE_STATUS: OPERATIONAL")
