from PIL import Image

img = Image.open("original_motherboard.jpg")
print(f"Original size: {img.size}")

# Let's crop key regions and save them so we can verify exact pixel coordinates:
# 1. 24-pin ATX header (usually on the right edge, middle-top)
# 2. SATA ports (usually on the right edge, lower)
# 3. CPU power (top left)
# 4. RAM slots (right of CPU socket)
# 5. Front panel header (bottom right corner)

# We can crop right edge: x from 900 to 1376, y from 200 to 768
crop_right = img.crop((850, 150, 1376, 768))
crop_right.save("scratch_crop_right.jpg")

# Top left:
crop_topleft = img.crop((300, 0, 850, 450))
crop_topleft.save("scratch_crop_topleft.jpg")

print("Cropped regions saved.")
