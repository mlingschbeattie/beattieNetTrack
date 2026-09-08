from PIL import Image, ImageDraw, ImageFont

def add_grid(img_path, out_path, orig_x, orig_y):
    img = Image.open(img_path).convert("RGB")
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
    w, h = img.size

    for x in range(0, w, 50):
        actual_x = orig_x + x
        d.line([(x, 0), (x, h)], fill=(100, 100, 100))
        d.text((x + 2, 5), str(actual_x), fill=(255, 255, 0), font=f)

    for y in range(0, h, 50):
        actual_y = orig_y + y
        d.line([(0, y), (w, y)], fill=(100, 100, 100))
        d.text((5, y + 2), str(actual_y), fill=(255, 255, 0), font=f)

    img.save(out_path)

add_grid("scratch_crop_right.jpg", "grid_crop_right.jpg", 850, 150)
add_grid("scratch_crop_topleft.jpg", "grid_crop_topleft.jpg", 300, 0)
print("Grid images generated.")
