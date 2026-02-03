import streamlit as st
import random

# --- CONFIG & STYLING ---
st.set_page_config(page_title="AQUASINE v20.5 - GLITCH HEX", layout="wide")

# Custom CSS für den Dark-Cyberpunk Look
st.markdown("""
    <style>
    .main { background-color: #000000; color: #00ffcc; }
    .stTextArea textarea { background-color: #050505 !important; color: #00ffcc !important; font-family: 'Courier New', monospace; border: 1px solid #111; }
    .stTextInput input { background-color: #0a0a0a !important; color: #ff0055 !important; font-family: 'Courier New', monospace; text-align: center; border: 1px solid #333; }
    .stButton>button { width: 100%; background-color: #0a0a0a; color: #00ffcc; border: 1px solid #00ffcc; border-radius: 0; transition: 0.3s; }
    .stButton>button:hover { background-color: #00ffcc; color: black; }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Courier', monospace; }
    .status-text { color: #444; font-family: 'Courier', monospace; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIK ---
GLYPH_BASE = 0x2200
RANGE_SIZE = 256

def process_logic(content, seed_val):
    if not content:
        return ""
    
    # Check ob verschlüsselt oder entschlüsselt werden soll
    is_decrypt = len(content) > 0 and GLYPH_BASE <= ord(content[0]) < (GLYPH_BASE + RANGE_SIZE + 500)
    
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

# --- UI LAYOUT ---
def main():
    st.title("◈ AQUASINE v20.5 - GLITCH HEX")
    
    # Sidebar für Steuerung
    with st.sidebar:
        st.markdown("### GLITCH_HEX")
        
        if st.button("[ RE-SEED ]"):
            st.session_state.seed = random.randint(10000, 99999)
        
        if 'seed' not in st.session_state:
            st.session_state.seed = 42839
            
        seed_str = st.text_input("[ ENTROPY_SEED ]", value=str(st.session_state.seed))
        seed_val = int(''.join(filter(str.isdigit, seed_str)) or 0)

        st.markdown("---")
        st.markdown('<p class="status-text">◈ NODE_READY</p>', unsafe_allow_html=True)

    # Hauptbereich
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### INPUT_STREAMS")
        input_data = st.text_area("Input", height=300, label_visibility="collapsed", placeholder="Enter data to glitch...")

    # Berechnung
    output_data, status = process_logic(input_data, seed_val)

    with col2:
        st.markdown(f"### OUTPUT_STREAMS ({status})")
        st.text_area("Output", value=output_data, height=300, label_visibility="collapsed")
        
        if st.button("[ COPY TO CLIPBOARD ]"):
            # In Streamlit ist direktes Copy-to-Clipboard schwierig ohne JS, 
            # aber man kann den Text einfach markieren oder ein st.code Block nutzen
            st.info("Mark den Text oben zum Kopieren.")

    st.markdown(f'<p class="status-text" style="text-align: center;">◈ CURRENT_SEED: {seed_val} | STATUS: {status}</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
