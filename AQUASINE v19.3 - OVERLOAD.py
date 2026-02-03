# -------------------------------------------------------------------------
# AQUASINE v19.3 - OVERLOAD 
# Developed by: vehmkater & Gemini (AI Collaboration)
# License: Non-Commercial Source License (c) 2026
# "Where aesthetic meets decryption"
# -------------------------------------------------------------------------

import tkinter as tk
import random
import hashlib

class AquasineOverload:
    def __init__(self, root):
        self.root = root
        self.root.title("AQUASINE v19.3 - OVERLOAD")
        self.root.geometry("1200x950")
        self.root.configure(bg="#020202")

        # Der massive Pool aus v19.2 + Erweiterungen
        self.pool = [
            '⪁','⫘','⽊','⯐','⇩','ⵓ','⶛','⥀','⎕','ⱘ','Ⰴ','⣹','⮏','⿋','ⳙ','⇷','✁',
            '⛗','ⳃ','⧑','≬','⌊','⊍','⓱','▢','⧌','⹷','⡘','⾸','≰','⏠','⋯','⫩','⡵',
            '⾡','⨀','⅚','⭩','⣚','Ⱁ','⵮','⋇','➻','⣨','⫫','✼','⼻','⡠','⻲','Ⲻ','Ⲭ',
            '⾤','☫','⑫','⌋','⟣','ⱺ','⽁','␤','ⵀ','℘','⸹','⡪','ⷃ','⩱','╽','⋊','⒟',
            '⫄','⛖','⍷','⣙','Ⱶ','Ⅵ','⪊','Ⳏ','⢾','ⷆ','␓','⟘','⣓','♜','❼','⍞','⽰',
            '⼚','⮡','⇊','Ⱨ','⏦','⺬','⨾','⮹','⬉','☼','⦠','►','⮇','⯊','ⲝ','∽','⌙','⊐',
            'ꒈ','꓀','ꑿ','ꐦ','ꆜ','ꈶ','ꉔ','ꊈ','ꋪ','ꍖ','ꏂ','ꑰ','ꓷ','ꔒ','ꖴ','ꗾ','ꘚ','ꚩ',
            'ᚙ','᚛','ᚚ','ᚠ','ᚢ','ᚦ','ᚨ','ᚱ','ᚳ','ᚵ','ᚷ','ᚻ','ᚽ','ᛃ','ᛄ','ᛇ','ᛈ','ᛉ',
            'ⵗ','ⵘ','ⵙ','ⵚ','ⵛ','ⵜ','ⵝ','ⵞ','ⵟ','ⵠ','ⵡ','ⵢ','ⵣ','ⵤ','ⵥ','ⵦ','ⵧ','⵨',
            '⢀','⢁','⢂','⢃','⢄','⢅','⢆','⢇','⢈','⢉','⢊','⢋','⢌','⢍','⢎','⢏','⢐',
            '⠿','⠾','⠽','⠼','⠻','⠺','⠹','⠸','⠷','⠶','⠵','⠴','⠳','⠲','⠱','⠰','⠯'
        ]
        
        # Deine Glitch-Marks für die physische Zerstörung
        self.glitch_marks = ['\u0334', '\u0338', '\u033f', '\u0322', '\u0352', '\u0360', '\u0361', '\u0488', '\u0489']
        
        self.mode = "ENCRYPT"
        self.setup_ui()

    def get_map(self, seed):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789.,!? ()-/%:;#\n"
        rng = random.Random(seed)
        shuffled = self.pool[:]
        rng.shuffle(shuffled)
        c2s, s2c = {}, {}
        for i, c in enumerate(chars):
            s = shuffled[i % len(shuffled)]
            while s in s2c: s += chr(0x200B)
            c2s[c] = s
            s2c[s] = c
        return c2s, s2c

    def setup_ui(self):
        # Sidebar
        side = tk.Frame(self.root, bg="#000", width=220, highlightbackground="#1a1a1a", highlightthickness=1)
        side.pack(side="left", fill="y")

        tk.Label(side, text="AQUASINE_VOID", fg="#00ffcc", bg="#000", font=("Consolas", 14, "bold")).pack(pady=25)

        tk.Label(side, text="[ SEED_KEY ]", fg="#444", bg="#000", font=("Consolas", 8)).pack()
        self.seed_ent = tk.Entry(side, bg="#080808", fg="#ff0055", borderwidth=0, insertbackground="white", justify="center", font=("Consolas", 11))
        self.seed_ent.insert(0, str(random.randint(1000000000, 9999999999)))
        self.seed_ent.pack(padx=15, pady=5, fill="x")
        self.seed_ent.bind("<KeyRelease>", lambda e: self.process())

        tk.Button(side, text="🎲 RANDOM_SEED", bg="#0a0a0a", fg="#00ffcc", relief="flat", command=self.randomize_seed).pack(fill="x", padx=25, pady=10)

        tk.Frame(side, height=1, bg="#222").pack(fill="x", pady=25)

        self.btn = tk.Button(side, text="[ ENCRYPT ]", bg="#0a0a0a", fg="#ff0055", font=("Consolas", 11, "bold"), relief="flat", command=self.toggle)
        self.btn.pack(fill="x", pady=10)

        # CHAOS CONTROL
        tk.Label(side, text="[ CHAOS_LEVEL ]", fg="#444", bg="#000", font=("Consolas", 8)).pack(pady=(20,0))
        self.chaos_var = tk.DoubleVar(value=0.4)
        tk.Scale(side, from_=0, to=1.0, resolution=0.1, variable=self.chaos_var, bg="#000", fg="#ff0055", highlightthickness=0, orient="horizontal", command=lambda x: self.process()).pack(fill="x", padx=20)

        tk.Button(side, text="[ SECURE_WIPE ]", bg="#150000", fg="#ff4444", relief="flat", command=self.secure_wipe).pack(fill="x", side="bottom", pady=30)

        # Text Interface
        main = tk.Frame(self.root, bg="#020202")
        main.pack(side="right", expand=True, fill="both")

        self.in_txt = tk.Text(main, bg="#000", fg="#00ffcc", font=("Consolas", 12), height=12, insertbackground="#ff0055", borderwidth=0, padx=20, pady=20)
        self.in_txt.pack(fill="both", expand=True, padx=25, pady=(25, 10))
        self.in_txt.bind("<KeyRelease>", self.process)

        self.out_txt = tk.Text(main, bg="#000", fg="#ff0055", font=("Consolas", 16), wrap="char", borderwidth=0, padx=20, pady=20)
        self.out_txt.pack(fill="both", expand=True, padx=25, pady=(10, 25))

    def randomize_seed(self):
        self.seed_ent.delete(0, tk.END)
        self.seed_ent.insert(0, str(random.randint(1000000000, 9999999999)))
        self.process()

    def secure_wipe(self):
        self.in_txt.delete("1.0", tk.END)
        self.randomize_seed()

    def toggle(self):
        self.mode = "DECRYPT" if self.mode == "ENCRYPT" else "ENCRYPT"
        self.btn.config(text=f"[ {self.mode} ]")
        self.process()

    def process(self, event=None):
        raw = self.in_txt.get("1.0", "end-1c")
        c2s, s2c = self.get_map(self.seed_ent.get())
        chaos = self.chaos_var.get()
        
        if self.mode == "ENCRYPT":
            cursor = len(self.in_txt.get("1.0", tk.INSERT))
            res = []
            for i, c in enumerate(raw.lower()):
                if i == cursor - 1: res.append("⌖")
                sym = c2s.get(c, c)
                
                # Overload / Glitch Logic
                if c in c2s and chaos > 0:
                    random.seed(i + int(self.seed_ent.get() or 0))
                    if random.random() < chaos:
                        for _ in range(random.randint(1, int(chaos * 5))):
                            sym += random.choice(self.glitch_marks)
                res.append(sym)
            out = "".join(res)
        else:
            # Reinigung von Diakritika vor dem Decodieren
            clean_text = raw
            for mark in self.glitch_marks:
                clean_text = clean_text.replace(mark, "")
            
            # Normales Decodieren
            out = clean_text
            for s in sorted(s2c.keys(), key=len, reverse=True):
                out = out.replace(s, s2c[s])

        self.out_txt.config(state="normal")
        self.out_txt.delete("1.0", "end")
        self.out_txt.insert("1.0", out)
        self.out_txt.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk(); app = AquasineOverload(root); root.mainloop()
