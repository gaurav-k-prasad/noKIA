import numpy as np
from PIL import Image


def apply_color_map(input_file, output_file):
    # 1. Load the numpy array
    data = np.load(input_file)

    # 2. Normalize data to a 0.0 - 1.0 range
    d_min, d_max = data.min(), data.max()
    if d_max == d_min:
        norm_data = np.zeros_like(data)
    else:
        norm_data = (data - d_min) / (d_max - d_min)

    # 3. Create the RGB channels
    # Logic:
    # Blue: High at 0.0, drops to 0 at 0.5
    # Green: High at 0.5, drops at 0.0 and 1.0
    # Red: High at 1.0, drops to 0 at 0.5

    r = np.clip((norm_data - 0.5) * 2, 0, 1)
    g = np.clip(1 - np.abs(norm_data - 0.5) * 2, 0, 1)
    b = np.clip((0.5 - norm_data) * 2, 0, 1)

    # 4. Stack channels into a (Height, Width, 3) uint8 array
    rgb = np.zeros((*norm_data.shape, 3), dtype=np.uint8)
    rgb[..., 0] = (r * 255).astype(np.uint8)
    rgb[..., 1] = (g * 255).astype(np.uint8)
    rgb[..., 2] = (b * 255).astype(np.uint8)

    # 5. Save as PNG
    Image.fromarray(rgb).save(output_file)
    print(f"Successfully saved colored map to {output_file}")


# Usage:
apply_color_map("sparse_hills_map.npy", "colored_map.png")
