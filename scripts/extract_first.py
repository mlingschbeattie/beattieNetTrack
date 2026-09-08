import subprocess
from PIL import Image

with open("motherboard_0b78809.jpg", "wb") as f:
    subprocess.run(["git", "show", "0b78809:public/images/hardware/motherboard-atx-landmarks.jpg"], stdout=f)

img = Image.open("motherboard_0b78809.jpg")
print("0b78809 image size:", img.size)
