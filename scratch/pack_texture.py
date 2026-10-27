import base64, io
from PIL import Image

content = open('docs/assets/cobe.js', 'r', encoding='utf-8').read()
b64 = content.split('base64,')[1].split('"')[0]
data = base64.b64decode(b64)
img = Image.open(io.BytesIO(data)).convert('L')
pixels = list(img.getdata())

# Pack 8 pixels into 1 byte (1 for land > 128, 0 for ocean)
bit_bytes = bytearray(len(pixels) // 8)
for i in range(len(pixels)):
    if pixels[i] > 128:
        byte_idx = i // 8
        bit_idx = 7 - (i % 8)
        bit_bytes[byte_idx] |= (1 << bit_idx)

bit_b64 = base64.b64encode(bit_bytes).decode('ascii')
print("Packed bit b64 len:", len(bit_b64), "Bytes:", len(bit_bytes))

# Now let's inject this decode into cobe.js
# Replace onSetup texture creation
setup_code_old = """onSetup:r=>{let a=r.RGB,o=r.UNSIGNED_BYTE,n=r.TEXTURE_2D,f=r.createTexture();r._globeTexture=f;r.bindTexture(n,f),r.texImage2D(n,0,a,1,1,0,a,o,new Uint8Array([0,0,0,0]));let l=new Image;l.onload=()=>{r.bindTexture(n,f),r.texImage2D(n,0,a,a,o,l),r.generateMipmap(n);let u=r.getParameter(r.CURRENT_PROGRAM),k=u?r.getUniformLocation(u,"J"):null;r.texParameteri(n,r.TEXTURE_MIN_FILTER,r.NEAREST),r.texParameteri(n,r.TEXTURE_MAG_FILTER,r.NEAREST);if(k)r.uniform1i(k,0);r.activeTexture(r.TEXTURE0);r.bindTexture(n,f);};l.src="data:image/png;base64,"""

# Let's search where onSetup starts and l.src ends in docs/assets/cobe.js
start_idx = content.find("onSetup:r=>{")
src_idx = content.find('l.src="data:image/png;base64,', start_idx)
end_idx = content.find('"', src_idx + len('l.src="data:image/png;base64,')) + 2 # include semicolon

print("Found onSetup from", start_idx, "to", end_idx)

new_setup = f"""onSetup:r=>{{let n=r.TEXTURE_2D,f=r.createTexture();r._globeTexture=f;let s=atob("{bit_b64}"),p=new Uint8Array(32768);for(let i=0;i<s.length;i++){{let b=s.charCodeAt(i);for(let k=7;k>=0;k--)p[i*8+(7-k)]=(b&(1<<k))?255:0;}}r.activeTexture(r.TEXTURE0);r.bindTexture(n,f);r.texImage2D(n,0,r.LUMINANCE,256,128,0,r.LUMINANCE,r.UNSIGNED_BYTE,p);r.texParameteri(n,r.TEXTURE_MIN_FILTER,r.NEAREST);r.texParameteri(n,r.TEXTURE_MAG_FILTER,r.NEAREST);r.texParameteri(n,r.TEXTURE_WRAP_S,r.REPEAT);r.texParameteri(n,r.TEXTURE_WRAP_T,r.CLAMP_TO_EDGE);}}"""

new_content = content[:start_idx] + new_setup + content[end_idx:]
open('docs/assets/cobe.js', 'w', encoding='utf-8').write(new_content)
print("Updated docs/assets/cobe.js with synchronous 1-bit packed texture!")
