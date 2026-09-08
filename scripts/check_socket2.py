from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_motherboard.jpg").convert("RGB")
crop = img.crop((550, 150, 850, 450))
d = ImageDraw.Draw(crop)
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)

# If original is (705, 270), in crop (starts at 550, 150), it is (155, 120)
cx, cy = 705 - 550, 270 - 150
d.ellipse([cx-12, cy-12, cx+12, cy+12], outline=(0, 255, 255), width=3)
d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(255, 255, 255))
d.text((cx + 15, cy - 8), "Dead Center", fill=(255, 255, 0), font=f)

crop.save("socket_center_check2.jpg")
print("Saved socket_center_check2.jpg")
