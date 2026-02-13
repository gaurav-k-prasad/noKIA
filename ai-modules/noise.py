import numpy as np
import opensimplex
from PIL import Image

# --- CONFIGURATION FOR SPARSE HILLS ---
WIDTH, HEIGHT = 800, 800
SCALE = 300.0  # High scale = larger distances between features
OCTAVES = 4
PERSISTENCE = 0.7
LACUNARITY = 2.0
SEED = 99
HILL_EXPONENT = 3.0  # HIGHER = Hills are further apart and steeper


def generate_sparse_hills(w, h, s, oct, pers, lac, seed, exp):
    gen = opensimplex.OpenSimplex(seed=seed)
    final_map = np.zeros((h, w))
    amp, freq, max_amp = 1.0, 1.0, 0

    for i in range(oct):
        x_idx = np.arange(w) * freq / s
        y_idx = np.arange(h) * freq / s
        final_map += opensimplex.noise2array(x_idx, y_idx) * amp
        max_amp += amp
        amp *= pers
        freq *= lac

    # 1. Normalize to 0.0 - 1.0
    normalized = (final_map / max_amp + 1) / 2

    # 2. APPLY EXPONENT: This is the magic for "far apart"
    # Values near 0.0 stay near 0.0, but only values near 1.0 stay high.
    sparse_map = np.power(normalized, exp)

    return sparse_map


for i in range(1):
    # 1. Generate Data
    noise_data = generate_sparse_hills(
        WIDTH, HEIGHT, SCALE, OCTAVES, PERSISTENCE, LACUNARITY, SEED, HILL_EXPONENT
    )
    np.save(f"sparse_hills_map{i}.npy", noise_data)

    # 2. Visual Mapping
    color_map = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # Colors for a "Plains and Hills" look
    PLAINS = [120, 180, 100]  # Light green
    HILL_BASE = [80, 130, 70]  # Darker green
    PEAK = [120, 120, 120]  # Grey rock

    # Thresholding
    color_map[noise_data < 0.1] = PLAINS  # Most of the map will be this
    color_map[(noise_data >= 0.1) & (noise_data < 0.4)] = HILL_BASE
    color_map[noise_data >= 0.4] = PEAK

    # 3. Save
    Image.fromarray(color_map, "RGB").save(f"sparse_hills{i}.png")
    print(f"Map saved! {i} Use HILL_EXPONENT={HILL_EXPONENT} to adjust hill density.")
