import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide")

# --- INITIALISIERUNG ---
if 'seed' not in st.session_state:
    st.session_state.seed = random.randint(10000, 99999)
if 'output_cache' not in st.session_state:
    st.session_state.output_cache = ""

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #030303 !important; }
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
        border: 1px solid #111 !important;
    }
    .stButton>button { 
        width: 100%; background-color: #0a0a0a; color: #00ffcc; border: 1px solid #00ffcc; 
        font-family: 'Courier', monospace; height: 3em;
    }
    .stButton>button:hover { border: 1px solid #ff0055; color: #ff0055; }
    h3 { color: #00ffcc !important; font-family: 'Courier', monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIK ---
GLYPH_BASE = 0x2200
RANGE_SIZE = 256

def process_logic(content, seed_val):
    if not content or content.strip() == "":
        return "ERROR: NO_INPUT", "IDLE"
    
    # Check ob verschlüsselt oder entschlüsselt (anhand des ersten Zeichens)
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
    
    return res, "DECRYPTED" if is_decrypt else "ENCRYPTED"

# --- MAIN UI ---
def main():
    st.title("◈ AQUASINE v20.5 - NODE")

    with st.sidebar:
        st.markdown("### SYSTEM_CTRL")
        if st.button("[ NEW_SEED ]"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()
        
        seed_input = st.text_input("CURRENT_SEED", value=str(st.session_state.seed))
        try:
            current_seed = int(''.join(filter(str.isdigit, seed_input)) or 0)
        except:
            current_seed = 0
            
        st.markdown("---")
        if st.button("[ RESET_ALL ]"):
            st.session_state.output_cache = ""
            st.rerun()

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### INPUT_STREAM")
        user_input = st.text_area("Input", height=400, label_visibility="collapsed", key="input_key")
        
        # DER SENDEN BUTTON
        if st.button("◈ [ EXECUTE_PROCESS ] ◈"):
            output, status = process_logic(user_input, current_seed)
            st.session_state.output_cache = output
            st.session_state.status_cache = status
            st.rerun()

    with col2:
        status_label = st.session_state.get('status_cache', 'IDLE')
        st.markdown(f"### OUTPUT_STREAM ({status_label})")
        
        # Zeigt den gespeicherten Output an
        st.text_area(
            "Output", 
            value=st.session_state.output_cache, 
            height=400, 
            label_visibility="collapsed", 
            key="output_key"
        )

    st.markdown(f"---")
    st.caption(f"AQUASINE CORE | SEED: {current_seed} | NODE: ACTIVE")

if __name__ == "__main__":
    main()
