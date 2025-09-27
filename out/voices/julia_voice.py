# JULIA Voice - fractal texture
# FX Chain: lfo, reverb
# Tempo: 140.0 BPM
# Harmony Note: G

------------------------------
for i in range(16):
    _fractal_depth = 3
    fractal_process(i, _fractal_depth)
    process_julia(i)
   Type: fractal
   Description: Recursive texture, code 'folds in on itself'
   Visual: recursive_patterns (#059669)