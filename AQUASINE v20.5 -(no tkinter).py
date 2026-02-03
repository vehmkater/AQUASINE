import streamlit as st
import random

# --- CONFIG & STYLING ---
st.set_page_config(page_title="AQUASINE v20.5", layout="wide")

# Custom CSS für das "Glitch-Hex" Design
st.markdown("""
    <style>
    /* Hintergrund und Grundfarben */
    .stApp { background-color: #000000; color: #00ffcc; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #030303 !important; border-right: 1px solid #111; }
    
    /* Textfelder */
    .stTextArea textarea { 
        background-color: #000000 !important; 
        color: #00ffcc !important; 
        font-family: 'Courier New', monospace !important; 
        border: 1px solid #111 !important; 
        padding: 20px !important;
    }
    
    /* Output Feld Farbe (Pink/Rot wie im Original) */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) .stTextArea textarea {
        color: #ff0055 !important;
    }

    /* Input Felder für Seed */
    .stTextInput input { 
        background-color: #0a0a0a !important; 
        color: #ff0055 !important; 
        font-family: 'Courier', monospace !important; 
        text-align: center !important; 
        border: 1px solid #333 !important; 
    }

    /* Buttons */
    .stButton>button { 
        width: 100%; 
        background-color: #0a0a0a; 
        color: #00ffcc; 
        border: 1px solid #00ffcc; 
        border-radius: 0; 
        font-family: 'Courier', monospace;
    }
    .stButton>button:hover { background-color: #00ffcc; color: black; border: 1px solid #00ffcc; }
    
    /* Überschriften */
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Courier', monospace; font-weight: bold; }
    .status-msg { color: #444; font-family: 'Courier', monospace; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIK ---
GLYPH_BASE = 0x2200
RANGE_SIZE = 256

def process_logic(content, seed_val):
    """Verarbeitet die Verschlüsselung/Entschlüsselung."""
    if not content:
        return "", "NODE_IDLE"
    
    # Erkennung: Ist das erste Zeichen aus dem Glyphen-Block?
    is_decrypt = GLYPH_BASE <= ord(content[0]) < (GLYPH_BASE + RANGE_SIZE + 500)
    
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
    
    status = "DECRYPTING..." if is_decrypt else "ENCRYPTING..."
    return res, status

# --- MAIN UI ---
def main():
    # Sidebar Setup
    with st.sidebar:
        st.markdown("### GLITCH_HEX")
        st.markdown("---")
        
        # Seed Management
        if 'seed' not in st.session_state:
            st.session_state.seed = random.randint(10000, 99999)
            
        if st.button("[ RE-SEED ]"):
            st.session_state.seed = random.randint(10000, 99999)
            st.rerun()

        seed_input = st.text_input("[ ENTROPY_SEED ]", value=str(st.session_state.seed))
        
        # Extrahiere nur Zahlen aus dem Input
        seed_digits = ''.join(filter(str.isdigit, seed_input))
        current_seed = int(seed_digits) if seed_digits else 0
        
        st.markdown("---")
        st.markdown('<p class="status-msg">◈ AQUASINE CORE V20.5</p>', unsafe_allow_html=True)

    # Layout Spalten
    st.markdown("### ◈ NODE_INTERFACE")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### [ INPUT_STREAM ]")
        input_text = st.text_area(
            "Input", 
            height=400, 
            label_visibility="collapsed", 
            placeholder="Warte auf Daten-Input...",
            key="input_area"
        )

    # Logik ausführen
    output_text, status_msg = process_logic(input_text, current_seed)

    with col2:
        st.markdown(f"#### [ OUTPUT_STREAM : {status_msg} ]")
        st.text_area(
            "Output", 
            value=output_text, 
            height=400, 
            label_visibility="collapsed", 
            key="output_area"
        )

    # Footer Status
    footer_color = "#ff9100" if "DECRYPT" in status_msg else "#00ffcc"
    st.markdown(f"""
        <p style="text-align: center; font-family: 'Courier', monospace; color: {footer_color}; padding-top: 20px;">
        ◈ STATUS: {status_msg} | ACTIVE_SEED: {current_seed} ◈
        </p>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
