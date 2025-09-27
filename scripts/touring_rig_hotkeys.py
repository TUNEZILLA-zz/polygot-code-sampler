#!/usr/bin/env python3
"""
Touring Rig Hotkeys - LOLcat++ integration
"""
import requests
import time

API_BASE = "http://127.0.0.1:8787"


def post(path, payload):
    try:
        return requests.post(f"{API_BASE}{path}", json=payload, timeout=2).json()
    except:
        return {"error": "API not available"}


def toggle_module(module_name):
    """Toggle a module on/off"""
    return post("/rig/module/toggle", {"module": module_name})


def nudge_param(param_path, delta, min_val, max_val):
    """Nudge a parameter by delta, clamped to [min_val, max_val]"""
    return post(
        "/rig/param/nudge",
        {"param": param_path, "delta": delta, "min": min_val, "max": max_val},
    )


def set_param(param_path, value):
    """Set a parameter to a specific value"""
    return post("/rig/param", {"key": param_path, "value": value})


# LOLcat++ hotkeys
HOTKEYS = {
    "L": {"desc": "LOLcat layer toggle", "cmd": lambda: toggle_module("lolcat_plus")},
    ";": {
        "desc": "LOLcat emoji -",
        "cmd": lambda: nudge_param("lolcat_plus.emoji", -0.02, 0.0, 0.2),
    },
    "'": {
        "desc": "LOLcat emoji +",
        "cmd": lambda: nudge_param("lolcat_plus.emoji", +0.02, 0.0, 0.2),
    },
    "[": {
        "desc": "LOLcat chaos -",
        "cmd": lambda: nudge_param("lolcat_plus.chaos", -0.03, 0.0, 0.5),
    },
    "]": {
        "desc": "LOLcat chaos +",
        "cmd": lambda: nudge_param("lolcat_plus.chaos", +0.03, 0.0, 0.5),
    },
    "\\": {
        "desc": "LOLcat uwu -",
        "cmd": lambda: nudge_param("lolcat_plus.uwu", -0.05, 0.0, 1.0),
    },
    "|": {
        "desc": "LOLcat uwu +",
        "cmd": lambda: nudge_param("lolcat_plus.uwu", +0.05, 0.0, 1.0),
    },
    "{": {
        "desc": "LOLcat trail -",
        "cmd": lambda: nudge_param("lolcat_plus.trail", -0.05, 0.0, 0.6),
    },
    "}": {
        "desc": "LOLcat trail +",
        "cmd": lambda: nudge_param("lolcat_plus.trail", +0.05, 0.0, 0.6),
    },
}


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 touring_rig_hotkeys.py <key>")
        print("Available keys:")
        for key, info in HOTKEYS.items():
            print(f"  {key}: {info['desc']}")
        return

    key = sys.argv[1]
    if key in HOTKEYS:
        result = HOTKEYS[key]["cmd"]()
        print(f"Executed: {HOTKEYS[key]['desc']}")
        if "error" in result:
            print(f"Error: {result['error']}")
    else:
        print(f"Unknown key: {key}")


if __name__ == "__main__":
    main()
