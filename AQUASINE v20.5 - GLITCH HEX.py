import tkinter as tk
import random

class HexNodeV20_5:
    def __init__(self, root):
        self.root = root
        self.root.title("AQUASINE v20.5 - GLITCH HEX")
        self.root.geometry("1100x850")
        self.root.configure(bg="#000000")

        # Wir nutzen einen Bereich mit hoher Dichte an interessanten Glyphen:
        # 0x2A00 (Mathematische Operatoren) bis 0x2C00
        self.glyph_base = 0x2A00 
        self.range_size = 512 # Wir bleiben in einem stabilen 512-Zeichen Fenster
        
        self.setup_ui()
        self.generate_new_seed()

    def setup_ui(self):
        self.sidebar = tk.Frame(self.root, bg="#030303", width=220)
        self.sidebar.pack(side="left", fill="y")
        
        tk.Label(self.sidebar, text="GLITCH_HEX", bg="#030303", fg="#00ffcc", font=("Courier", 16, "bold")).pack(pady=40)
        
        # Seed
        tk.Label(self.sidebar, text="[ ENTROPY_SEED ]", bg="#030303", fg="#444", font=("Courier", 9)).pack()
        self.seed_entry = tk.Entry(self.sidebar, bg="#0a0a0a", fg="#ff0055", font=("Courier", 12), bd=0, justify="center")
        self.seed_entry.pack(pady=10, padx=20, fill="x")
        self.seed_entry.bind("<KeyRelease>", lambda e: self.process())

        btn_style = {"bg": "#0a0a0a", "fg": "#00ffcc", "font": ("Courier", 10, "bold"), "bd": 0, "cursor": "hand2", "activebackground": "#111"}
        tk.Button(self.sidebar, text="[ RE-SEED ]", command=self.generate_new_seed, **btn_style).pack(pady=15, padx=25, fill="x")
        tk.Button(self.sidebar, text="[ COPY ]", command=self.copy_output, **btn_style).pack(pady=15, padx=25, fill="x")

        self.status_label = tk.Label(self.sidebar, text="◈ NODE_IDLE", bg="#030303", fg="#222", font=("Courier", 8))
        self.status_label.pack(side="bottom", pady=20)

        # Content Zone
        self.main_frame = tk.Frame(self.root, bg="#000000")
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.input_text = tk.Text(self.main_frame, bg="#000000", fg="#00ffcc", insertbackground="#00ffcc", font=("Courier New", 13), bd=0, padx=45, pady=30, undo=True)
        self.input_text.pack(fill="both", expand=True)
        self.input_text.bind("<KeyRelease>", self.auto_process)

        tk.Frame(self.main_frame, height=1, bg="#111").pack(fill="x")

        self.output_text = tk.Text(self.main_frame, bg="#000000", fg="#ff0055", font=("Courier New", 13), bd=0, padx=45, pady=30)
        self.output_text.pack(fill="both", expand=True)

    def generate_new_seed(self):
        self.seed_entry.delete(0, tk.END)
        self.seed_entry.insert(0, str(random.randint(10000, 99999)))
        self.process()

    def copy_output(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.output_text.get("1.0", "end-1c"))
        self.status_label.config(text="◈ COPIED", fg="#ff9100")

    def auto_process(self, event):
        if event.keysym not in ("Left", "Right", "Up", "Down"):
            self.process()

    def process(self):
        content = self.input_text.get("1.0", "end-1c")
        if not content:
            self.output_text.delete("1.0", "end")
            return

        seed_val = int(''.join(filter(str.isdigit, self.seed_entry.get())) or "0")
        
        # Erkennung durch Code-Point-Check
        is_decrypt = len(content) > 0 and self.glyph_base <= ord(content[0]) <= (self.glyph_base + self.range_size + 1000)
        
        self.status_label.config(text="◈ DECRYPTING..." if is_decrypt else "◈ ENCRYPTING...", fg="#555")

        res = ""
        for i, char in enumerate(content):
            if char in (" ", "\n"):
                res += char
                continue
            
            # Positioneller Zufallsshift
            char_rng = random.Random(seed_val + i)
            shift = char_rng.randint(1, 1000)

            if not is_decrypt:
                # ENCRYPT: Sicherer Wrap-around
                new_code = self.glyph_base + (ord(char) + shift) % self.range_size
                res += chr(new_code)
            else:
                # DECRYPT: Mathematische Umkehrung
                glyph_code = ord(char)
                orig_code = (glyph_code - self.glyph_base - shift) % self.range_size
                # ASCII/Unicode-Reconstruction (Versuch, in den lesbaren Bereich zu mappen)
                # Da Modulo verlustbehaftet sein kann, ist dies ein 'best-fit' für v20.5
                res += chr(orig_code % 1114111) 

        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", res)

if __name__ == "__main__":
    root = tk.Tk()
    app = HexNodeV20_5(root)
    root.mainloop()
