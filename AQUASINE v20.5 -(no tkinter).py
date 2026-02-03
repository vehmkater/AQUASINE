import streamlit as st
import random

# --- CONFIG & STYLING ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide")

# Custom CSS für maximale Kompatibilität und Look
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    section[data-testid="stSidebar"] { background-color: #030303 !important; }
    
    /* Input Area */
    .stTextArea textarea { 
        background-color: #050505 !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
    }
    
    /* Code Block (Output) Styling */
    code { color: #ff0055 !important; background-color: #0a0a0a !important; }
    
    .stButton>button { 
        width: 100%; background-color: #0a0a0a; color: #00ffcc; border: 1px solid #00ffcc; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIK ---
GLYPH_BASE = 0x2200
RANGE_SIZE = 256

def process_logic(content, seed_val):
    if not content or content.strip() == "":
        return "", "NODE_IDLE"
    
    # Check ob verschlüsselt oder entschlüsselt (Glyphen Check)
    first_char_code = ord(content.strip()[0])
    is_decrypt = GLYPH_BASE <= first_char_code < (GLYPH_BASE + RANGE_SIZE + 500)
    
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

# --- MAIN UI ---
def main():
    st.title("◈ AQUASINE v20.5")

    # Sidebar
    with st.sidebar:
        st.header("CONTROLS")
        if 'seed' not in st.session_state:
            st.session_state.seed = random.randint(10000, 99999)
            
        if st.button("[ GENERATE NEW SEED ]"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()

        seed_input = st.text_input("SEED", value=str(st.session_state.seed))
        
        try:
            current_seed = int(''.join(filter(str.isdigit, seed_input)) or 0)
        except:
            current_seed = 0

    # Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("INPUT_STREAM")
        # Das 'key' Argument sorgt dafür, dass Streamlit den State trackt
        user_input = st.text_area("Input Area", height=400, label_visibility="collapsed", key="main_input")

    # Berechnung triggern
    output_text, status_msg = process_logic(user_input, current_seed)

    with col2:
        st.subheader(f"OUTPUT_STREAM: {status_msg}")
        if output_text:
            # Wir nutzen st.code für bessere Sichtbarkeit oder st.text_area
            st.text_area("Output Area", value=output_text, height=400, label_visibility="collapsed", key="main_output")
            st.button("Copy Ready", disabled=True)
        else:
            st.info("System bereit. Bitte Text eingeben.")

    # Footer
    st.markdown("---")
    st.caption(f"Kernel: Active | Seed: {current_seed} | Mode: {status_msg}")

if __name__ == "__main__":
    main()
