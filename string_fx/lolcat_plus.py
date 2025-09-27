# string_fx/lolcat_plus.py
import re, random, math
from typing import Dict

DEFAULT_EMOJIS = ["😺","😸","😹","😻","✨","🌈","🐾","🫶","🍣"]

# Emoji palettes by scene theme
EMOJI_PALETTES = {
    "default": ["😺","😸","😹","😻","✨","🌈","🐾","🫶","🍣"],
    "cyberpunk": ["🟣","💜","🔮","⚡","🌟","💫","🔯","🎆","🌌"],
    "gold": ["🟡","✨","⭐","🌟","💛","🏆","👑","💎","🔆"],
    "emerald": ["🟢","💚","🌿","🍀","🌱","🌾","🌳","🌲","🌿"],
    "neon": ["💖","💗","💘","💝","💞","💟","💠","💡","💎"],
    "vintage": ["📻","🎵","🎶","🎼","🎹","🎺","🎷","🎸","🎻"]
}
REWRITE = [
    (re.compile(r"\bthe\b", re.I), "teh"),
    (re.compile(r"\byou\b", re.I), "u"),
    (re.compile(r"\byour\b", re.I), "ur"),
    (re.compile(r"\bwith\b", re.I), "wif"),
    (re.compile(r"\breally\b", re.I), "rly"),
    (re.compile(r"\blittle\b", re.I), "lil"),
    (re.compile(r"\bsmall\b", re.I), "smol"),
    (re.compile(r"\bawesome\b", re.I), "pawsome"),
    (re.compile(r"ing\b", re.I), "in'")
]

def _uwuify(s: str, amt: float) -> str:
    if amt <= 0: return s
    s = re.sub(r"[rl]", "w", s)
    s = re.sub(r"[RL]", "W", s)
    if amt > 0.5:
        s = s.replace("na", "nya").replace("Na","Nya")
    return s

def _stretch_vowels(word: str, amt: float, seed: int) -> str:
    random.seed((hash(word) ^ seed) & 0xFFFFFFFF)
    if amt <= 0: return word
    def rep(m):
        base = m.group(0)
        k = 1 + int(amt * 4)  # up to ~5 repeats
        return base * (1 + random.randint(0, k))
    return re.sub(r"[aeiouAEIOU]", rep, word, count=1)

def _chaos_case(token: str, amt: float, seed: int) -> str:
    if amt <= 0: return token
    random.seed((seed ^ hash(token)) & 0xFFFFFFFF)
    out = []
    wobble = max(1, int(6 - amt*4))
    up = random.choice([True, False])
    for i,ch in enumerate(token):
        if ch.isalpha() and i % wobble == 0:
            up = not up
        out.append(ch.upper() if up and ch.isalpha() else ch.lower())
    return "".join(out)

def _sprinkle_emojis(tokens, density: float, seed: int, emojis=DEFAULT_EMOJIS):
    if density <= 0: return tokens
    random.seed(seed)
    out = []
    for t in tokens:
        out.append(t)
        if random.random() < density:
            out.append(random.choice(emojis))
    return out

def _gradient_ansi(s: str, phase: float=0.0, mono: bool=False) -> str:
    if mono: return s
    out = []
    for i,ch in enumerate(s):
        # simple HSV->RGB rainbow
        h = (phase + i*0.03) % 1.0
        r,g,b = [int(c*255) for c in _hsv_to_rgb(h, 0.9, 1.0)]
        out.append(f"\x1b[38;2;{r};{g};{b}m{ch}")
    out.append("\x1b[0m")
    return "".join(out)

def _hsv_to_rgb(h,s,v):
    i = int(h*6); f = h*6 - i; p=v*(1-s); q=v*(1-f*s); t=v*(1-(1-f)*s); i%=6
    return [(v,q,p,t,p,q)[i], (t,v,q,p,q,p)[i], (p,p,t,q,v,t)[i]]

def lolcat_plus(text: str, *, intensity: float=0.6, seed: int=1337,
                uwu: float=0.4, chaos: float=0.2, emoji: float=0.15,
                gradient_phase: float=0.0, mono: bool=False,
                reduced_motion: bool=False, nyan_trail: float=0.0,
                emoji_palette: str="default", content_guard: bool=True) -> Dict:
    """
    Returns dict with { 'text': str, 'ansi': str } so the rack can choose.
    """
    rnd = random.Random(seed)
    
    # 0) Content Guard - skip LOLcat++ inside back-ticked code/URLs
    if content_guard:
        # Find and protect back-ticked code blocks
        protected_regions = []
        protected_text = text
        
        # Protect back-ticked code (```code```)
        code_blocks = re.findall(r'```[^`]*```', text)
        for i, block in enumerate(code_blocks):
            placeholder = f"__PROTECTED_CODE_{i}__"
            protected_text = protected_text.replace(block, placeholder)
            protected_regions.append((placeholder, block))
        
        # Protect URLs (http://, https://, ftp://)
        url_pattern = r'https?://[^\s]+|ftp://[^\s]+'
        urls = re.findall(url_pattern, protected_text)
        for i, url in enumerate(urls):
            placeholder = f"__PROTECTED_URL_{i}__"
            protected_text = protected_text.replace(url, placeholder)
            protected_regions.append((placeholder, url))
        
        # Protect inline code (`code`)
        inline_code = re.findall(r'`[^`]+`', protected_text)
        for i, code in enumerate(inline_code):
            placeholder = f"__PROTECTED_INLINE_{i}__"
            protected_text = protected_text.replace(code, placeholder)
            protected_regions.append((placeholder, code))
            
        # Protect the placeholders themselves from transformation
        # Use a pattern that won't be affected by LOLcat++ transformations
        for i, (placeholder, original) in enumerate(protected_regions):
            protected_text = protected_text.replace(placeholder, f"__{i}__")
    else:
        protected_text = text
        protected_regions = []
    
    # 1) rule rewrites
    out = protected_text
    for pat, repl in REWRITE:
        out = pat.sub(repl, out)

    # 2) uwu
    out = _uwuify(out, uwu)

    # 3) purr & stretch per word (scaled by intensity)
    words = re.findall(r"\w+|\W+", out)
    words = [ _stretch_vowels(w, intensity*0.6, seed) if re.match(r"\w", w) else w
             for w in words ]

    # 4) chaos case
    words = [ _chaos_case(w, chaos, seed) if re.match(r"[A-Za-z]", w) else w for w in words ]

    # 5) emojis (A11y aware)
    dens = 0 if reduced_motion else emoji
    emoji_set = EMOJI_PALETTES.get(emoji_palette, DEFAULT_EMOJIS)
    sprinkled = _sprinkle_emojis(words, dens, seed, emoji_set)

    plain = "".join(sprinkled)

    # 6) gradient color (ANSI) – mono respected
    ansi = _gradient_ansi(plain, phase=gradient_phase, mono=mono)

    # 7) Restore protected regions
    if content_guard and protected_regions:
        for i, (placeholder, original) in enumerate(protected_regions):
            # Restore the protected placeholders
            protected_placeholder = f"__{i}__"
            plain = plain.replace(protected_placeholder, original)
            ansi = ansi.replace(protected_placeholder, original)

    # 8) optional nyan trail marker (your engine can render ghosts)
    trail = max(0.0, min(nyan_trail, 1.0))
    meta = {"trail": trail, "seed": seed, "intensity": intensity, "content_guard": content_guard}

    return {"text": plain, "ansi": ansi, "meta": meta}
