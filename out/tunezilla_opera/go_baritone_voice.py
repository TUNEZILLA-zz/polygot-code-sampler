# GO_BARITONE Voice - TuneZilla Opera
# Emerald Mask - Wave Pattern
# Crow Layers: 1, Lizard Clones: 1

# ✦ sparse foundation ✦
# go's steady rhythm
# emerald pulses

def go_baritone_voice():
    # Sparse, minimal emerald baritone
    for i in range(8):
        process_sparse(i, voice_config.volume)
        if i % 2 == 0:
            emerald_pulse(i)
        if i % 4 == 0:
            crow_minimal(i)