from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_motherboard.jpg").convert("RGB")
d = ImageDraw.Draw(img)

# Let's inspect points:
# (1050, 345)
# (1055, 655)
# (910, 265)
# (600, 610)
# (650, 530)

pts = {
    "ATX_24PIN": (1050, 345),
    "SATA": (1055, 655),
    "RAM": (910, 265),
    "GPU_PCIE": (600, 610),
    "M2_NVME": (650, 530),
    "CPU_SOCKET": (710, 335),
    "CPU_EPS": (510, 70),
    "REAR_IO": (340, 330),
    "PCIE_SLOTS": (490, 690),
    "FRONT_AUDIO": (500, 725),
    "FRONT_PANEL": (960, 695)
}

f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
for name, (x, y) in pts.items():
    d.ellipse([x-10, y-10, x+10, y+10], outline=(255, 0, 0), width=3)
    d.text((x + 12, y - 7), name, fill=(255, 255, 0), font=f)

img.save("debug_motherboard_points.jpg")
print("Saved debug_motherboard_points.jpg")
