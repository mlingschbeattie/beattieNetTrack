import os
from PIL import Image, ImageDraw, ImageFont

# Load clean original motherboard image
src_path = "original_motherboard.jpg"
if not os.path.exists(src_path):
    import subprocess
    with open(src_path, "wb") as f:
        subprocess.run(["git", "show", "HEAD~2:public/images/hardware/motherboard-atx-landmarks.jpg"], stdout=f)

base = Image.open(src_path).convert("RGBA")

# Target canvas: 2280 x 1120 gives massive room for large, bold, high-contrast text
CANVAS_W = 2280
CANVAS_H = 1120

OFFSET_X = 430
OFFSET_Y = 150

canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (11, 17, 32, 255))
canvas.paste(base, (OFFSET_X, OFFSET_Y))

overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Large, highly legible typography
font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
font_subhdr = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)

# High-contrast theme tokens
COLORS = {
    "COMPUTE":  {"border": (56, 189, 248, 255), "bg": (14, 30, 52, 250),  "accent": (56, 189, 248, 255), "glow": (56, 189, 248, 90)},
    "POWER":    {"border": (251, 191, 36, 255), "bg": (42, 30, 10, 250),  "accent": (251, 191, 36, 255), "glow": (251, 191, 36, 90)},
    "GPU":      {"border": (192, 132, 252, 255), "bg": (36, 18, 54, 250), "accent": (192, 132, 252, 255), "glow": (192, 132, 252, 90)},
    "STORAGE":  {"border": (52, 211, 153, 255), "bg": (12, 40, 28, 250),  "accent": (52, 211, 153, 255), "glow": (52, 211, 153, 90)},
    "IO":       {"border": (244, 63, 94, 255),  "bg": (48, 14, 25, 250),  "accent": (244, 63, 94, 255), "glow": (244, 63, 94, 90)},
    "EXPANSION":{"border": (129, 140, 248, 255), "bg": (22, 25, 58, 250), "accent": (129, 140, 248, 255), "glow": (129, 140, 248, 90)},
    "CHASSIS":  {"border": (148, 163, 184, 255), "bg": (26, 32, 44, 250), "accent": (148, 163, 184, 255), "glow": (148, 163, 184, 90)},
}

# Header banner at top
draw.text((40, 25), "ATX MOTHERBOARD INTERFACE & HARDWARE LANDMARK MAP", fill=(248, 250, 252), font=font_header)
draw.text((42, 62), "CompTIA A+ Core 1 physical reference: identifying where each subsystem connects to the system board.", fill=(148, 163, 184), font=font_subhdr)

# Helper function to convert board relative coordinates to canvas
def b2c(bx, by):
    return (bx + OFFSET_X, by + OFFSET_Y)

# Calibrated physical board anchors:
# CPU EPS: (510, 70)
# CPU Socket: (710, 335)
# Rear I/O: (340, 330)
# PCIe Expansion: (490, 690)
# Front Audio: (500, 725)
# DDR5 RAM: (910, 265)
# 24-Pin ATX: (1050, 345)
# M.2 NVMe: (650, 530)
# PCIe 5.0 x16 (GPU): (600, 610)
# SATA 6Gbps: (1055, 655)
# Front Panel: (960, 695)

callouts = [
    # Top Left: CPU EPS Power
    {
        "category": "POWER",
        "title": "8+8 Pin CPU Power (EPS 12V)",
        "plugs": "Plugs: Dedicated 8-Pin CPU 12V power cables from PSU",
        "box": (30, 110, 400, 68),
        "anchor": b2c(510, 70),
        "path": [(430, 144), (b2c(510, 70)[0], 144), b2c(510, 70)],
    },
    # Top Center: CPU Socket
    {
        "category": "COMPUTE",
        "title": "CPU Socket (LGA 1700)",
        "plugs": "Plugs: Processor (Intel Core 12th-14th Gen) under ZIF lever",
        "box": (940, 22, 420, 68),
        "anchor": b2c(710, 335),
        "path": [(1140, 90), b2c(710, 335)],
    },
    # Left 2: Rear I/O Panel
    {
        "category": "IO",
        "title": "Rear I/O External Ports",
        "plugs": "Plugs: Monitors (DP/HDMI), 2.5GbE LAN, USB, Audio",
        "box": (30, 300, 400, 68),
        "anchor": b2c(340, 330),
        "path": [(430, 334), (b2c(340, 330)[0], 334), b2c(340, 330)],
    },
    # Left 3: PCIe Expansion Slots
    {
        "category": "EXPANSION",
        "title": "PCIe Expansion Slots (x1 / x4)",
        "plugs": "Plugs: Add-in cards (Wi-Fi, 10GbE NICs, Sound, Capture)",
        "box": (30, 540, 400, 68),
        "anchor": b2c(490, 690),
        "path": [(430, 574), (550, 574), (550, b2c(490, 690)[1]), b2c(490, 690)],
    },
    # Left 4: Front Audio & Case Headers
    {
        "category": "CHASSIS",
        "title": "Front Panel Audio & USB Headers",
        "plugs": "Plugs: Case Front USB 2.0/3.2 and HD Audio cables",
        "box": (30, 780, 400, 68),
        "anchor": b2c(500, 725),
        "path": [(430, 814), (520, 814), (520, b2c(500, 725)[1]), b2c(500, 725)],
    },
    # Right 1: DDR5 RAM Slots
    {
        "category": "COMPUTE",
        "title": "DDR5 Memory Slots (DIMM 1-4)",
        "plugs": "Plugs: System RAM sticks (Dual-Channel Priority A2/B2)",
        "box": (1850, 110, 400, 68),
        "anchor": b2c(910, 265),
        "path": [(1850, 144), (1730, 144), (1730, b2c(910, 265)[1]), b2c(910, 265)],
    },
    # Right 2: 24-Pin ATX Main Power
    {
        "category": "POWER",
        "title": "24-Pin ATX Main Power Header",
        "plugs": "Plugs: Main 24-Pin harness from PSU (powers board & chipset)",
        "box": (1850, 280, 400, 68),
        "anchor": b2c(1050, 345),
        "path": [(1850, 314), (1670, 314), (1670, b2c(1050, 345)[1]), b2c(1050, 345)],
    },
    # Right 3: M.2 NVMe SSD Slot (Gen 5)
    {
        "category": "STORAGE",
        "title": "M.2 NVMe PCIe SSD Slot (Gen 5)",
        "plugs": "Plugs: High-speed M.2 2280 NVMe SSD (under heatsink)",
        "box": (1850, 450, 400, 68),
        "anchor": b2c(650, 530),
        "path": [(1850, 484), (1630, 484), (1630, b2c(650, 530)[1]), b2c(650, 530)],
    },
    # Right 4: Primary PCIe 5.0 x16 Slot
    {
        "category": "GPU",
        "title": "PCIe 5.0 x16 Slot (Steel Armor)",
        "plugs": "Plugs: Dedicated Graphics Card (Discrete GPU)",
        "box": (1850, 620, 400, 68),
        "anchor": b2c(600, 610),
        "path": [(1850, 654), (1590, 654), (1590, b2c(600, 610)[1]), b2c(600, 610)],
    },
    # Right 5: SATA 6Gbps Storage Ports
    {
        "category": "STORAGE",
        "title": "SATA 6Gbps Storage Ports",
        "plugs": "Plugs: SATA Data cables to 2.5\" SSDs & 3.5\" Hard Drives",
        "box": (1850, 790, 400, 68),
        "anchor": b2c(1055, 655),
        "path": [(1850, 824), (1670, 824), (1670, b2c(1055, 655)[1]), b2c(1055, 655)],
    },
    # Right 6: Front Panel Switch/LED Header
    {
        "category": "CHASSIS",
        "title": "Front Panel Switch/LED Header",
        "plugs": "Plugs: Case Power Switch, Reset Button, HDD & Power LEDs",
        "box": (1850, 960, 400, 68),
        "anchor": b2c(960, 695),
        "path": [(1850, 994), (1710, 994), (1710, b2c(960, 695)[1]), b2c(960, 695)],
    },
]

def draw_badge(draw, c, box):
    x, y, w, h = box
    col = COLORS[c["category"]]

    # Dark background pill with soft rounded corners
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=col["bg"], outline=col["border"], width=2)

    # Category tag pill
    cat_text = c["category"]
    cat_w = draw.textlength(cat_text, font=font_badge)
    tag_x = x + 14
    tag_y = y + 10
    draw.rounded_rectangle([tag_x, tag_y, tag_x + cat_w + 14, tag_y + 19], radius=4, fill=col["border"])
    draw.text((tag_x + 7, tag_y + 2), cat_text, fill=(11, 17, 32), font=font_badge)

    # Title text (large 17px bold)
    title_x = tag_x + cat_w + 20
    draw.text((title_x, y + 9), c["title"], fill=(248, 250, 252), font=font_title)

    # Subtitle / Plugs text (14px clean)
    draw.text((x + 16, y + 38), c["plugs"], fill=(203, 213, 225), font=font_subtitle)

def draw_trace(draw, c):
    col = COLORS[c["category"]]
    points = c["path"]
    ax, ay = c["anchor"]

    # Wide glow line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["glow"], width=7)

    # Sharp trace line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["border"], width=3)

    # Target anchor ring directly on the physical hardware port
    draw.ellipse([ax - 12, ay - 12, ax + 12, ay + 12], fill=col["glow"])
    draw.ellipse([ax - 7, ay - 7, ax + 7, ay + 7], fill=col["border"], outline=(255, 255, 255, 255), width=2)
    draw.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=(255, 255, 255, 255))

# Draw all traces first
for c in callouts:
    draw_trace(draw, c)

# Draw all badges on top
for c in callouts:
    draw_badge(draw, c, c["box"])

# Composite overlay
final_img = Image.alpha_composite(canvas, overlay).convert("RGB")
output_path = "public/images/hardware/motherboard-atx-landmarks.jpg"
final_img.save(output_path, quality=95)
print(f"Successfully generated enlarged diagram with massive readability to {output_path}")
