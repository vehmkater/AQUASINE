import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide")

# --- SESSION STATE INITIALISIERUNG ---
# Das sorgt dafür, dass Eingaben nicht verschwinden
if 'input_val' not in st.session_state:
    st.session_state.input_val = ""
if 'seed' not in st.session_state:
    st.session_state.seed = random.randint(10000, 99999)

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #030303 !important; }
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
    }
    /* Output Feld in Pink */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) .stTextArea textarea {
        color: #ff0055 !important;
    }
    .stButton>button { 
        width: 100%; background-color: #0a0a0a; color: #00ffcc; border: 1px solid #00ffcc; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIK ---
GLYPH_BASE = 0x2200
RANGE_SIZE = 256

def process_logic(content, seed_val):
    if not content:
        return "", "NODE_IDLE"
    
    # Check ob verschlüsselt oder entschlüsselt
    stripped = content.strip()
    if not stripped: return "", "NODE_IDLE"
    
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
    
    return res, "DECRYPTING" if is_decrypt else "ENCRYPTING"

# --- UI FUNKTIONEN ---
def clear_text():
    st.session_state.input_val = ""

# --- MAIN UI ---
def main():
    st.title("◈ AQUASINE v20.5")

    with st.sidebar:
        st.header("CONTROLS")
        if st.button("[ GENERATE NEW SEED ]"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()

        seed_input = st.text_input("SEED", value=str(st.session_state.seed))
        try:
            current_seed = int(''.join(filter(str.isdigit, seed_input)) or 0)
        except:
            current_seed = 0
            
        st.markdown("---")
        if st.button("[ CLEAR ALL ]"):
            clear_text()
            st.rerun()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("INPUT_STREAM")
        # Das TextArea nutzt nun den Session State
        user_input = st.text_area(
            "Input Area", 
            value=st.session_state.input_val,
            height=400, 
            label_visibility="collapsed", 
            key="input_field"
        )
        # Update den State sofort
        st.session_state.input_val = user_input

    # Berechnung
    output_text, status_msg = process_logic(st.session_state.input_val, current_seed)

    with col2:
        st.subheader(f"OUTPUT_STREAM: {status_msg}")
        st.text_area(
            "Output Area", 
            value=output_text, 
            height=400, 
            label_visibility="collapsed", 
            key="output_field"
        )

    st.caption(f"Status: {status_msg} | Seed: {current_seed}")

if __name__ == "__main__":
    main()
