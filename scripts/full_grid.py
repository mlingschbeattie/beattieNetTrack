from PIL import Image

# Let's inspect the area around x=1000..1150, y=250..700
# On a typical ATX board:
# RAM is to the right of the CPU socket.
# The 24-pin power connector is immediately to the right of the RAM slots, along the edge.
# SATA ports are along the right edge below the 24-pin connector, usually right-angled or vertical.

# Let's crop a tight 200x200 around candidate areas and print mean color
img = Image.open("original_motherboard.jpg")
w, h = img.size

# Let's save a full labeled grid on the whole motherboard!
from PIL import ImageDraw, ImageFont

d = ImageDraw.Draw(img)
f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
for x in range(0, w, 100):
    d.line([(x, 0), (x, h)], fill=(70, 70, 70))
    d.text((x + 2, 8), str(x), fill=(0, 255, 255), font=f)
for y in range(0, h, 100):
    d.line([(0, y), (w, y)], fill=(70, 70, 70))
    d.text((8, y + 2), str(y), fill=(0, 255, 255), font=f)

img.save("full_motherboard_grid.jpg")
print("Saved full_motherboard_grid.jpg")
