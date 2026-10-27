import base64, io
from PIL import Image

content = open('docs/assets/cobe.js', 'r', encoding='utf-8').read()
b64 = content.split('base64,')[1].split('"')[0]
data = base64.b64decode(b64)
img = Image.open(io.BytesIO(data))
print("Image size:", img.size, "Mode:", img.mode)
print("Bytes:", len(data))
