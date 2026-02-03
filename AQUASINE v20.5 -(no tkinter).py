import streamlit as st
import random

# Page Config für den "Glitch"-Look
st.set_page_config(page_title="AQUASINE v20.5", layout="wide")

# CSS für das Dark-Design (ähnlich wie dein Tkinter-Theme)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00ffcc; }
    textarea { background-color: #0a0a0a !important; color: #00ffcc !important; font-family: 'Courier New', monospace !important; }
    .stButton>button { background-color: #0a0a0a; color: #00ffcc; border: 1px solid #00ffcc; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

def process_logic(content, seed_val):
    glyph_base = 0x2200 
    range_size = 256
    
    if not content: return ""
    
    # Erkennung ob Verschlüsselt oder nicht
    is_decrypt = glyph_base <= ord(content[0]) < (glyph_base + range_size + 500)
    
    res = ""
    for i, char in enumerate(content):
        if char in (" ", "\n"):
            res += char
            continue
        
        char_rng = random.Random(seed_val + i)
        shift = char_rng.randint(1, 1000)

        if not is_decrypt:
            new_code = glyph_base + (ord(char) + shift) % range_size
            res += chr(new_code)
        else:
            glyph_code = ord(char)
            orig_code = (glyph_code - glyph_base - shift) % range_size
            res += chr(orig_code % 256)
    return res

# Sidebar UI
with st.sidebar:
    st.title("GLITCH_HEX")
    st.write("[ ENTROPY_SEED ]")
    seed = st.text_input("Seed", value="55555", label_visibility="collapsed")
    if st.button("[ RE-SEED ]"):
        seed = str(random.randint(10000, 99999))
    
    st.markdown("---")
    st.caption("◈ NODE_ACTIVE")

# Main UI
st.title("AQUASINE v20.5 - GLITCH HEX")

col1, col2 = st.columns(2)

with col1:
    st.subheader("INPUT")
    user_input = st.text_area("Input Zone", height=400, label_visibility="collapsed", key="input")

# Berechnung
try:
    seed_int = int(''.join(filter(str.isdigit, seed)))
except:
    seed_int = 0

output_data = process_logic(user_input, seed_int)

with col2:
    st.subheader("OUTPUT")
    st.text_area("Output Zone", value=output_data, height=400, label_visibility="collapsed", key="output")

if st.button("[ COPY OUTPUT ]"):
    st.write("Kopiere den Text einfach manuell aus dem rechten Feld.")
