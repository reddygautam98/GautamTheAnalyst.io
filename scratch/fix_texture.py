import base64, io
from PIL import Image

content = open('docs/assets/cobe.js', 'r', encoding='utf-8').read()
b64 = content.split('base64,')[1].split('"')[0]
data = base64.b64decode(b64)
img = Image.open(io.BytesIO(data))
print("Original format:", img.format, "size:", img.size, "mode:", img.mode)

# Convert to standard RGB (or L grayscale 8-bit)
img_rgb = img.convert('RGB')
out = io.BytesIO()
img_rgb.save(out, format='PNG')
new_data = out.getvalue()
new_b64 = base64.b64encode(new_data).decode('ascii')

print("Old b64 len:", len(b64), "New b64 len:", len(new_b64))
new_content = content.replace(b64, new_b64)
open('docs/assets/cobe.js', 'w', encoding='utf-8').write(new_content)
print("Successfully replaced cobe.js texture with 8-bit RGB PNG!")
