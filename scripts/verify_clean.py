from PIL import Image

raw = Image.open("raw_motherboard.jpg")
print("Raw size:", raw.size)

# Let's save a clean copy to original_motherboard.jpg
raw.save("original_motherboard.jpg", quality=98)
print("Saved clean original_motherboard.jpg")
