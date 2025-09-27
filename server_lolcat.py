# server_lolcat.py - Code Live with Lolcat FX Rack
import random
import re
import time
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel


# Lolcat FX Rack Models
class LolcatFXRequest(BaseModel):
    target: str
    code: str
    parallel: bool = False
    rainbow_speed: float = 0.5
    color_phase: float = 0.25
    cat_density: float = 0.3
    success_cats: bool = True
    angry_cats: bool = False
    owoifier: bool = False
    comic_sans: bool = False
    catify: bool = False
    chaos_level: float = 0.2
    tail_wag_speed: float = 0.4
    zoomies_mode: bool = False
    purr_freq: float = 0.6
    nyan_mode: bool = False
    nyan_speed: float = 0.7
    cat_jam: bool = False
    ceiling_cat: bool = False
    glitch_cats: bool = False


class LolcatFXResponse(BaseModel):
    code: str
    notes: List[str] = []
    degraded: bool = False
    metrics: Dict[str, Any]
    warnings: List[str] = []
    fallbacks: List[str] = []
    lolcat_effects: Dict[str, Any] = {}


# Lolcat FX Rack Implementation
class LolcatFX:
    def __init__(self):
        self.cat_emojis = [
            "🐱",
            "🐈",
            "😸",
            "😹",
            "😺",
            "😻",
            "😼",
            "😽",
            "😾",
            "😿",
            "🙀",
        ]
        self.success_cats = ["=^.^=", "=^w^=", "=^_^=", "=^o^="]
        self.angry_cats = [">:3", ">:(", ">:O", ">:P"]
        self.owo_patterns = [
            (r"\bif\b", "ifUwU"),
            (r"\bfor\b", "fowUwU"),
            (r"\bwhile\b", "whiweUwU"),
            (r"\bdef\b", "defUwU"),
            (r"\bclass\b", "cwassUwU"),
            (r"\breturn\b", "wetuwnUwU"),
            (r"\bprint\b", "pwintUwU"),
            (r"\binput\b", "inputUwU"),
            (r"\brange\b", "wangeUwU"),
            (r"\blen\b", "wenUwU"),
            (r"\bstr\b", "stwUwU"),
            (r"\bint\b", "intUwU"),
            (r"\bfloat\b", "fwoatUwU"),
            (r"\blist\b", "wistUwU"),
            (r"\bdict\b", "dictUwU"),
            (r"\bset\b", "setUwU"),
            (r"\btuple\b", "tupweUwU"),
            (r"\bTrue\b", "TwueUwU"),
            (r"\bFalse\b", "FawseUwU"),
            (r"\bNone\b", "NoneUwU"),
            (r"\band\b", "andUwU"),
            (r"\bor\b", "owUwU"),
            (r"\bnot\b", "notUwU"),
            (r"\bin\b", "inUwU"),
            (r"\bis\b", "isUwU"),
            (r"\bwith\b", "withUwU"),
            (r"\bas\b", "asUwU"),
            (r"\bfrom\b", "fwomUwU"),
            (r"\bimport\b", "impowtUwU"),
            (r"\bexcept\b", "exceptUwU"),
            (r"\btry\b", "twyUwU"),
            (r"\bfinally\b", "finawwyUwU"),
            (r"\braise\b", "waiseUwU"),
            (r"\bpass\b", "passUwU"),
            (r"\bbreak\b", "bweakUwU"),
            (r"\bcontinue\b", "continueUwU"),
            (r"\belse\b", "ewseUwU"),
            (r"\belif\b", "ewifUwU"),
            (r"\bif\b", "ifUwU"),
            (r"\bfor\b", "fowUwU"),
            (r"\bwhile\b", "whiweUwU"),
            (r"\bdef\b", "defUwU"),
            (r"\bclass\b", "cwassUwU"),
            (r"\breturn\b", "wetuwnUwU"),
            (r"\bprint\b", "pwintUwU"),
            (r"\binput\b", "inputUwU"),
            (r"\brange\b", "wangeUwU"),
            (r"\blen\b", "wenUwU"),
            (r"\bstr\b", "stwUwU"),
            (r"\bint\b", "intUwU"),
            (r"\bfloat\b", "fwoatUwU"),
            (r"\blist\b", "wistUwU"),
            (r"\bdict\b", "dictUwU"),
            (r"\bset\b", "setUwU"),
            (r"\btuple\b", "tupweUwU"),
            (r"\bTrue\b", "TwueUwU"),
            (r"\bFalse\b", "FawseUwU"),
            (r"\bNone\b", "NoneUwU"),
            (r"\band\b", "andUwU"),
            (r"\bor\b", "owUwU"),
            (r"\bnot\b", "notUwU"),
            (r"\bin\b", "inUwU"),
            (r"\bis\b", "isUwU"),
            (r"\bwith\b", "withUwU"),
            (r"\bas\b", "asUwU"),
            (r"\bfrom\b", "fwomUwU"),
            (r"\bimport\b", "impowtUwU"),
            (r"\bexcept\b", "exceptUwU"),
            (r"\btry\b", "twyUwU"),
            (r"\bfinally\b", "finawwyUwU"),
            (r"\braise\b", "waiseUwU"),
            (r"\bpass\b", "passUwU"),
            (r"\bbreak\b", "bweakUwU"),
            (r"\bcontinue\b", "continueUwU"),
            (r"\belse\b", "ewseUwU"),
            (r"\belif\b", "ewifUwU"),
        ]

    def apply_rainbow_filter(self, code: str, speed: float, phase: float) -> str:
        """Apply rainbow filter to code"""
        lines = code.split("\n")
        rainbow_lines = []

        for i, line in enumerate(lines):
            if line.strip():
                # Create rainbow effect based on line number and phase
                hue = (i * 30 + phase * 360) % 360
                rainbow_line = f"// 🌈 Rainbow line {i + 1} 🌈\n{line}"
                rainbow_lines.append(rainbow_line)
            else:
                rainbow_lines.append(line)

        return "\n".join(rainbow_lines)

    def apply_ascii_cats(
        self, code: str, density: float, success: bool, angry: bool
    ) -> str:
        """Add ASCII cat overlays"""
        lines = code.split("\n")
        cat_lines = []

        for i, line in enumerate(lines):
            cat_lines.append(line)

            # Add cats based on density
            if random.random() < density:
                if success and "success" in line.lower():
                    cat = random.choice(self.success_cats)
                    cat_lines.append(f"// {cat} Purr-fect success! {cat}")
                elif angry and ("error" in line.lower() or "fail" in line.lower()):
                    cat = random.choice(self.angry_cats)
                    cat_lines.append(f"// {cat} Hiss! Error detected! {cat}")
                else:
                    cat = random.choice(self.success_cats)
                    cat_lines.append(f"// {cat} Code generation {cat}")

        return "\n".join(cat_lines)

    def apply_owoifier(self, code: str) -> str:
        """Apply OwOifier to code"""
        owo_code = code

        for pattern, replacement in self.owo_patterns:
            owo_code = re.sub(pattern, replacement, owo_code)

        return owo_code

    def apply_comic_sans(self, code: str) -> str:
        """Apply Comic Sans styling (simulated with comments)"""
        lines = code.split("\n")
        comic_lines = []

        for line in lines:
            if line.strip():
                comic_lines.append(f"// 🎭 Comic Sans Mode: {line}")
            else:
                comic_lines.append(line)

        return "\n".join(comic_lines)

    def apply_catify(self, code: str) -> str:
        """Add cat function calls to code"""
        lines = code.split("\n")
        catified_lines = []

        for line in lines:
            catified_lines.append(line)

            # Add cat function calls
            if "def " in line or "function " in line:
                catified_lines.append("    meow()  // Cat function call")
                catified_lines.append("    purr()  // Cat satisfaction")
            elif "return " in line:
                catified_lines.append("    // 🐱 Cat approval granted")
            elif "if " in line:
                catified_lines.append("    // 🐈 Cat logic activated")

        return "\n".join(catified_lines)

    def apply_chaos(self, code: str, level: float) -> str:
        """Apply chaos effects"""
        if level < 0.3:
            return code

        lines = code.split("\n")
        chaos_lines = []

        for line in lines:
            chaos_lines.append(line)

            if level > 0.5:
                chaos_lines.append("// 🐈💨 CHAOS MODE ACTIVATED! 🐈💨")
            if level > 0.7:
                chaos_lines.append("// 🌈🚀 Nyan Cat is watching... 🚀🌈")
            if level > 0.9:
                chaos_lines.append("// 🐱💥 MAXIMUM CAT CHAOS! 💥🐱")

        return "\n".join(chaos_lines)

    def apply_nyan_mode(self, code: str, speed: float) -> str:
        """Apply Nyan Cat mode"""
        lines = code.split("\n")
        nyan_lines = []

        for i, line in enumerate(lines):
            if i % 3 == 0:  # Every 3rd line gets Nyan Cat
                nyan_lines.append("// 🚀🌈 Nyan Cat trail... 🌈🚀")
            nyan_lines.append(line)

        return "\n".join(nyan_lines)

    def apply_glitch_cats(self, code: str) -> str:
        """Apply glitch cat effects"""
        lines = code.split("\n")
        glitch_lines = []

        for line in lines:
            glitch_lines.append(line)

            # Add glitch cat comments
            if random.random() < 0.3:
                glitch_lines.append("// 🐱💫 Glitch cat detected! 💫🐱")

        return "\n".join(glitch_lines)

    def apply_cat_jam(self, code: str) -> str:
        """Apply cat jam effects"""
        lines = code.split("\n")
        jam_lines = []

        for line in lines:
            jam_lines.append(line)

            # Add cat jam comments
            if "def " in line or "function " in line:
                jam_lines.append("    // 🎵 Cat jam session started! 🎵")
            elif "return " in line:
                jam_lines.append("    // 🐱🎶 Cat jam complete! 🎶🐱")

        return "\n".join(jam_lines)

    def apply_ceiling_cat(self, code: str) -> str:
        """Apply ceiling cat effects"""
        lines = code.split("\n")
        ceiling_lines = []

        # Add ceiling cat at the top
        ceiling_lines.append("// 🐱 Ceiling Cat is watching your code... 🐱")
        ceiling_lines.append("// 🐱 Ceiling Cat approves of your logic! 🐱")

        for line in lines:
            ceiling_lines.append(line)

        return "\n".join(ceiling_lines)

    def process_code(self, code: str, fx_request: LolcatFXRequest) -> str:
        """Process code through the Lolcat FX Rack"""
        processed_code = code

        # Apply rainbow filter
        if fx_request.rainbow_speed > 0:
            processed_code = self.apply_rainbow_filter(
                processed_code, fx_request.rainbow_speed, fx_request.color_phase
            )

        # Apply ASCII cat overlays
        processed_code = self.apply_ascii_cats(
            processed_code,
            fx_request.cat_density,
            fx_request.success_cats,
            fx_request.angry_cats,
        )

        # Apply OwOifier
        if fx_request.owoifier:
            processed_code = self.apply_owoifier(processed_code)

        # Apply Comic Sans
        if fx_request.comic_sans:
            processed_code = self.apply_comic_sans(processed_code)

        # Apply Catify
        if fx_request.catify:
            processed_code = self.apply_catify(processed_code)

        # Apply chaos
        if fx_request.chaos_level > 0:
            processed_code = self.apply_chaos(processed_code, fx_request.chaos_level)

        # Apply Nyan Cat mode
        if fx_request.nyan_mode:
            processed_code = self.apply_nyan_mode(processed_code, fx_request.nyan_speed)

        # Apply glitch cats
        if fx_request.glitch_cats:
            processed_code = self.apply_glitch_cats(processed_code)

        # Apply cat jam
        if fx_request.cat_jam:
            processed_code = self.apply_cat_jam(processed_code)

        # Apply ceiling cat
        if fx_request.ceiling_cat:
            processed_code = self.apply_ceiling_cat(processed_code)

        return processed_code


# Create FastAPI app
app = FastAPI(
    title="Code Live - Lolcat FX Rack",
    description="The Ableton Live of Code + ShaderToy + Meme Engine",
    version="1.0.0",
    default_response_class=ORJSONResponse,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Lolcat FX
lolcat_fx = LolcatFX()


@app.post("/render/lolcat", response_model=LolcatFXResponse)
async def render_lolcat(request: LolcatFXRequest):
    """Render code with Lolcat FX Rack effects"""
    start_time = time.time()

    try:
        # Import renderers
        from pcs_step3_ts import (
            PyToIR,
            render_csharp,
            render_go,
            render_julia,
            render_rust,
            render_sql,
            render_ts,
        )

        # Parse to IR
        parser = PyToIR()
        ir = parser.parse(request.code)

        # Render based on target
        if request.target == "rust":
            code = render_rust(ir, parallel=request.parallel)
        elif request.target == "ts":
            code = render_ts(ir, parallel=request.parallel)
        elif request.target == "go":
            code = render_go(ir, parallel=request.parallel)
        elif request.target == "csharp":
            code = render_csharp(ir, parallel=request.parallel)
        elif request.target == "sql":
            code = render_sql(ir)
        elif request.target == "julia":
            code = render_julia(ir, parallel=request.parallel)
        else:
            raise ValueError(f"Unknown target: {request.target}")

        # Apply Lolcat FX Rack effects
        lolcat_code = lolcat_fx.process_code(code, request)

        # Calculate metrics
        duration = time.time() - start_time
        metrics = {
            "latency_ms": duration * 1000,
            "code_length": len(lolcat_code),
            "target": request.target,
            "parallel": request.parallel,
            "cached": False,
            "lolcat_effects_applied": True,
        }

        # Generate Lolcat effects summary
        lolcat_effects = {
            "rainbow_filter": request.rainbow_speed > 0,
            "ascii_cats": request.cat_density > 0,
            "owoifier": request.owoifier,
            "comic_sans": request.comic_sans,
            "catify": request.catify,
            "chaos_level": request.chaos_level,
            "nyan_mode": request.nyan_mode,
            "glitch_cats": request.glitch_cats,
            "cat_jam": request.cat_jam,
            "ceiling_cat": request.ceiling_cat,
        }

        # Generate notes
        notes = []
        if request.rainbow_speed > 0:
            notes.append("🌈 Rainbow filter applied!")
        if request.cat_density > 0:
            notes.append("🐱 ASCII cats added!")
        if request.owoifier:
            notes.append("OwO Code has been OwOified!")
        if request.comic_sans:
            notes.append("🎭 Comic Sans mode activated!")
        if request.catify:
            notes.append("🐱 Code has been catified!")
        if request.chaos_level > 0.5:
            notes.append("🐈💨 CHAOS MODE ACTIVATED!")
        if request.nyan_mode:
            notes.append("🚀🌈 Nyan Cat mode engaged!")
        if request.glitch_cats:
            notes.append("🐱💫 Glitch cats detected!")
        if request.cat_jam:
            notes.append("🎵 Cat jam session started!")
        if request.ceiling_cat:
            notes.append("🐱 Ceiling Cat is watching!")

        return LolcatFXResponse(
            code=lolcat_code,
            notes=notes,
            degraded=False,
            metrics=metrics,
            warnings=[],
            fallbacks=[],
            lolcat_effects=lolcat_effects,
        )

    except Exception as e:
        # Handle errors with cat-themed messages
        error_messages = [
            "🐱 Hiss! Something went wrong!",
            "😿 Cat is sad about this error!",
            "🙀 Cat is shocked by this failure!",
            "😾 Angry cat detected this problem!",
            "😿 Cat needs help with this code!",
        ]

        error_message = random.choice(error_messages)
        notes = [f"{error_message} {str(e)}"]

        return LolcatFXResponse(
            code=f"// {error_message}\n// Error: {str(e)}",
            notes=notes,
            degraded=True,
            metrics={
                "latency_ms": 0,
                "code_length": 0,
                "target": request.target,
                "parallel": request.parallel,
                "cached": False,
            },
            warnings=[str(e)],
            fallbacks=["error"],
            lolcat_effects={},
        )


@app.get("/health")
async def health():
    """Health check with cat theme"""
    return {
        "status": "ok",
        "message": "🐱 Code Live Lolcat FX Rack is purring! 🐱",
        "version": "1.0.0",
        "effects_available": [
            "🌈 Rainbow Filter",
            "🐱 ASCII Cat Overlays",
            "OwO OwOifier",
            "🎭 Comic Sans",
            "🐱 Catify",
            "🐈💨 Chaos Mode",
            "🚀🌈 Nyan Cat Mode",
            "🐱💫 Glitch Cats",
            "🎵 Cat Jam",
            "🐱 Ceiling Cat",
        ],
    }


@app.get("/")
async def root():
    """Root endpoint with cat welcome"""
    return {
        "message": "🐱 Welcome to Code Live Lolcat FX Rack! 🐱",
        "description": "The Ableton Live of Code + ShaderToy + Meme Engine",
        "endpoints": {"render": "/render/lolcat", "health": "/health"},
        "cat_facts": [
            "Cats can make over 100 different sounds!",
            "A group of cats is called a 'clowder'!",
            "Cats spend 70% of their lives sleeping!",
            "A cat's purr can help heal bones!",
            "Cats have a third eyelid called a nictitating membrane!",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8788)
