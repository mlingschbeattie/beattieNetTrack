from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_motherboard.jpg")
f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 10)

# Crop PCIe and M.2 area: X in [300, 700], Y in [450, 768]
crop = img.crop((300, 450, 700, 768))
w, h = crop.size
crop = crop.resize((w * 2, h * 2), Image.Resampling.NEAREST)

d = ImageDraw.Draw(crop)
for x in range(0, w, 20):
    d.line([(x*2, 0), (x*2, h*2)], fill=(80, 80, 80))
    d.text((x*2 + 1, 2), str(300 + x), fill=(255, 255, 0), font=f)

for y in range(0, h, 20):
    d.line([(0, y*2), (w*2, y*2)], fill=(80, 80, 80))
    d.text((2, y*2 + 1), str(450 + y), fill=(255, 255, 0), font=f)

crop.save("pcie_zoom.jpg")
print("Saved pcie_zoom.jpg")
