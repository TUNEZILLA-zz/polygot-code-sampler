# rack/modules.py
from string_fx.lolcat_plus import lolcat_plus

REGISTRY = {}

REGISTRY["lolcat_plus"] = {
    "apply": lambda text, p, ctx: lolcat_plus(
        text,
        intensity=p.get("intensity", 0.6),
        uwu=p.get("uwu", 0.4),
        chaos=p.get("chaos", 0.2),
        emoji=p.get("emoji", 0.12),
        gradient_phase=p.get("gradient_phase", 0.0 + ctx.get("phase", 0.0)),
        mono=ctx.get("mono", False) or p.get("mono", False),
        reduced_motion=ctx.get("reduced_motion", False)
        or p.get("reduced_motion", False),
        nyan_trail=p.get("trail", 0.0),
        seed=ctx.get("seed", 1337),
    )
}

# Default macro map for Pro Rack
LOLCAT_MACROS = {
    "macros": {
        "Color": [
            {
                "key": "lolcat_plus.gradient_phase",
                "min": 0.0,
                "max": 1.0,
                "curve": "linear",
            },
            {"key": "lolcat_plus.uwu", "min": 0.2, "max": 0.7, "curve": "soft_knee"},
            {"key": "lolcat_plus.emoji", "min": 0.05, "max": 0.20, "curve": "ease_out"},
        ],
        "Space": [
            {"key": "lolcat_plus.trail", "min": 0.0, "max": 0.6, "curve": "ease_in_out"}
        ],
        "Motion": [
            {"key": "lolcat_plus.chaos", "min": 0.0, "max": 0.5, "curve": "ease_in"}
        ],
        "Crunch": [{"key": "stutter.mix", "min": 0.0, "max": 0.25, "curve": "linear"}],
    }
}

# Sidechain metrics suggestions
LOLCAT_SIDECHAIN = {
    "qps": {"target": "lolcat_plus.gradient_phase", "slew": 0.8, "cap": 1.0},
    "error_rate": {"target": "lolcat_plus.chaos", "bump": 0.1, "fade": 200},
    "p95": {
        "target": "lolcat_plus.emoji",
        "multiplier": 0.75,
        "target2": "lolcat_plus.trail",
        "multiplier2": 0.75,
    },
}


# A11y auto-adjustments
def apply_a11y_adjustments(params, ctx):
    if ctx.get("reduced_motion", False):
        params["trail"] = 0.0
        params["emoji"] = min(params.get("emoji", 0.1), 0.05)
        params["mono"] = True
    return params
