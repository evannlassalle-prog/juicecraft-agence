import sys, glob, os
from PIL import Image, ImageDraw, ImageFont
d, out, cols, tw = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
fs = sorted(glob.glob(os.path.join(d, 't*.png')), key=lambda f: float(os.path.basename(f)[1:-4]))
ims = [Image.open(f) for f in fs]
w, h = ims[0].size; th = int(h * tw / w)
rows = (len(ims) + cols - 1) // cols
S = Image.new('RGB', (cols * (tw + 8) + 8, rows * (th + 30) + 8), (40, 40, 40))
dr = ImageDraw.Draw(S)
for i, (f, im) in enumerate(zip(fs, ims)):
    x, y = 8 + (i % cols) * (tw + 8), 8 + (i // cols) * (th + 30)
    S.paste(im.convert('RGB').resize((tw, th), Image.LANCZOS), (x, y + 22))
    dr.text((x, y + 4), os.path.basename(f)[1:-4] + ' s', fill=(255, 200, 120))
S.save(out)
print(out, S.size)
