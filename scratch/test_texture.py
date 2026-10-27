import base64, io
from PIL import Image

content = open('docs/assets/cobe.js', 'r', encoding='utf-8').read()
b64 = content.split('base64,')[1].split('"')[0]
data = base64.b64decode(b64)
img = Image.open(io.BytesIO(data)).convert('L')
pixels = list(img.getdata())
print("Total pixels:", len(pixels), "Width:", img.width, "Height:", img.height)
print("White pixels (land):", sum(1 for p in pixels if p > 128))
print("Black pixels (ocean):", sum(1 for p in pixels if p <= 128))

# Let's write the raw grayscale bytes as base64
raw_bytes = bytes([255 if p > 128 else 0 for p in pixels])
raw_b64 = base64.b64encode(raw_bytes).decode('ascii')
print("Raw b64 length:", len(raw_b64))

# Let's save this to a python test script
open("scratch/raw_map.py", "w").write(f'MAP_B64 = "{raw_b64}"\n')
print("Saved scratch/raw_map.py")
