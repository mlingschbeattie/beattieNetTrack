from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_motherboard.jpg")
f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 10)

# Crop X: 980 to 1100, Y: 500 to 768
crop = img.crop((980, 500, 1080, 768))
w, h = crop.size
crop = crop.resize((w * 3, h * 3), Image.Resampling.NEAREST)

d = ImageDraw.Draw(crop)
for x in range(0, w, 10):
    d.line([(x*3, 0), (x*3, h*3)], fill=(80, 80, 80))
    d.text((x*3 + 1, 2), str(980 + x), fill=(255, 255, 0), font=f)

for y in range(0, h, 10):
    d.line([(0, y*3), (w*3, y*3)], fill=(80, 80, 80))
    d.text((2, y*3 + 1), str(500 + y), fill=(255, 255, 0), font=f)

crop.save("sata_zoom.jpg")
print("Saved sata_zoom.jpg")
