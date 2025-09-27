# JULIA Voice - Act 2 in G major
# fractal texture with lfo, reverb FX

------------------------------
for i in range(16):
    _fractal_depth = 3
    fractal_process(i, _fractal_depth)
    process_julia(i)
   Type: fractal
   Description: Recursive texture, code 'folds in on itself'
   Visual: recursive_patterns (#059669)
    # Development: Enhanced fractal patterns
    for depth in range(2, 5):
        fractal_process(i, depth)