from PIL import Image, ImageDraw, ImageFont

img = Image.open("original_motherboard.jpg").convert("RGB")
d = ImageDraw.Draw(img)
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)

# CPU Socket test at (705, 400)
x, y = 705, 400
d.ellipse([x-12, y-12, x+12, y+12], outline=(0, 255, 255), width=3)
d.ellipse([x-3, y-3, x+3, y+3], fill=(255, 255, 255))
d.text((x + 15, y - 8), "CPU Socket Center", fill=(255, 255, 0), font=f)

crop = img.crop((550, 250, 850, 550))
crop.save("socket_center_check.jpg")
print("Saved socket_center_check.jpg")
