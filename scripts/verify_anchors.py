from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_motherboard.jpg").convert("RGB")
d = ImageDraw.Draw(img)
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)

anchors = {
    "CPU EPS (8+8 Pin 12V)": (545, 112),
    "CPU Socket (LGA 1700)": (690, 420),
    "Rear I/O": (260, 370),
    "PCIe x1": (465, 540),
    "Front Audio": (345, 715),
    "DDR5 RAM": (910, 360),
    "24-Pin ATX Power": (1050, 408),
    "M.2 NVMe": (620, 540),
    "PCIe 5.0 x16 (GPU)": (540, 612),
    "SATA 6Gbps": (1045, 655),
    "Front Panel Header": (995, 732),
}

for name, (x, y) in anchors.items():
    d.ellipse([x-12, y-12, x+12, y+12], outline=(0, 255, 255), width=3)
    d.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 255))
    d.line([(x-18, y), (x+18, y)], fill=(0, 255, 255), width=2)
    d.line([(x, y-18), (x, y+18)], fill=(0, 255, 255), width=2)
    d.text((x + 15, y - 8), name, fill=(255, 255, 0), font=f)

img.save("verify_anchors_preview.jpg")
print("Saved updated verify_anchors_preview.jpg")
