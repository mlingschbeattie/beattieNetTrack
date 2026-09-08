from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_motherboard.jpg")
f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)

# We want to find the exact location of:
# 1. 24-pin ATX connector
# 2. SATA ports

# Crop right side: x in [950, 1376], y in [150, 768]
crop = img.crop((950, 150, 1376, 768))
d = ImageDraw.Draw(crop)

# Draw grid every 25px
for x in range(0, crop.width, 25):
    d.line([(x, 0), (x, crop.height)], fill=(100, 100, 100, 120))
    d.text((x + 2, 2), str(950 + x), fill=(255, 255, 0), font=f)

for y in range(0, crop.height, 25):
    d.line([(0, y), (crop.width, y)], fill=(100, 100, 100, 120))
    d.text((2, y + 2), str(150 + y), fill=(255, 255, 0), font=f)

crop.save("grid_right_edge.jpg")
print("Saved grid_right_edge.jpg")
