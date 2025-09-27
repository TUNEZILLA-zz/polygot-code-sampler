# PYTHON_TENOR Voice - TuneZilla Opera
# Emerald Mask - Wave Pattern
# Crow Layers: 2, Lizard Clones: 1

# ✦ fracture in the loop ✦
# voices collide at 432hz
# emerald fog rises

def python_tenor_voice():
    # Smooth, flowing emerald tenor
    for i in range(16):
        process_smooth(i, voice_config.volume)
        if i % 4 == 0:
            crow_caw(i // 4)
        if i % 8 == 0:
            lizard_dance(i // 8)