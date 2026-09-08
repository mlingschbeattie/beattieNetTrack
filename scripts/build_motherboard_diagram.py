import os
from PIL import Image, ImageDraw, ImageFont

# Load clean original motherboard image
src_path = "original_motherboard.jpg"
if not os.path.exists(src_path):
    # Fallback to extracting from git if needed
    import subprocess
    with open(src_path, "wb") as f:
        subprocess.run(["git", "show", "HEAD:public/images/hardware/motherboard-atx-landmarks.jpg"], stdout=f)

base = Image.open(src_path).convert("RGBA")

# Canvas setup: 1860 x 940
CANVAS_W = 1860
CANVAS_H = 940
OFFSET_X = 240
OFFSET_Y = 85

canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (11, 17, 32, 255))
canvas.paste(base, (OFFSET_X, OFFSET_Y))

overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Fonts
font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_subhdr = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 9)

# Theme tokens
COLORS = {
    "COMPUTE":  {"border": (56, 189, 248, 255), "bg": (14, 30, 50, 248),  "accent": (56, 189, 248, 255), "glow": (56, 189, 248, 90)},
    "POWER":    {"border": (251, 191, 36, 255), "bg": (40, 30, 10, 248),  "accent": (251, 191, 36, 255), "glow": (251, 191, 36, 90)},
    "GPU":      {"border": (192, 132, 252, 255), "bg": (35, 18, 52, 248), "accent": (192, 132, 252, 255), "glow": (192, 132, 252, 90)},
    "STORAGE":  {"border": (52, 211, 153, 255), "bg": (12, 38, 28, 248),  "accent": (52, 211, 153, 255), "glow": (52, 211, 153, 90)},
    "IO":       {"border": (244, 63, 94, 255),  "bg": (45, 14, 24, 248),  "accent": (244, 63, 94, 255), "glow": (244, 63, 94, 90)},
    "EXPANSION":{"border": (129, 140, 248, 255), "bg": (22, 25, 55, 248), "accent": (129, 140, 248, 255), "glow": (129, 140, 248, 90)},
    "CHASSIS":  {"border": (148, 163, 184, 255), "bg": (24, 30, 42, 248), "accent": (148, 163, 184, 255), "glow": (148, 163, 184, 90)},
}

# Header banner
draw.text((30, 18), "ATX MOTHERBOARD INTERFACE & HARDWARE LANDMARK MAP", fill=(248, 250, 252), font=font_header)
draw.text((32, 45), "CompTIA A+ Core 1 physical reference: identifying where each subsystem connects to the system board.", fill=(148, 163, 184), font=font_subhdr)

# Calibrated Callouts with dedicated trace paths
callouts = [
    # Top Left: CPU EPS Power
    {
        "category": "POWER",
        "title": "8+8 Pin CPU Power (EPS 12V)",
        "plugs": "Plugs: Dedicated 8-Pin CPU 12V power cables from PSU",
        "box": (30, 85, 350, 54),
        "anchor": (750, 155),
        "path": [(380, 112), (750, 112), (750, 155)],
    },
    # Top Center: CPU Socket
    {
        "category": "COMPUTE",
        "title": "CPU Socket (LGA 1700)",
        "plugs": "Plugs: Processor (Intel Core 12th-14th Gen) under ZIF lever",
        "box": (800, 16, 380, 54),
        "anchor": (950, 420),
        "path": [(950, 70), (950, 420)],
    },
    # Left 2: Rear I/O Panel
    {
        "category": "IO",
        "title": "Rear I/O External Ports",
        "plugs": "Plugs: Monitors (DP/HDMI), 2.5GbE LAN, USB, Audio",
        "box": (30, 245, 350, 54),
        "anchor": (580, 415),
        "path": [(380, 272), (580, 272), (580, 415)],
    },
    # Left 3: PCIe Expansion Slots
    {
        "category": "EXPANSION",
        "title": "PCIe Expansion Slots (x1 / x4)",
        "plugs": "Plugs: Add-in cards (Wi-Fi, 10GbE NICs, Sound, Capture)",
        "box": (30, 440, 350, 54),
        "anchor": (730, 775),
        "path": [(380, 467), (460, 467), (460, 775), (730, 775)],
    },
    # Left 4: Front Audio & Case Headers
    {
        "category": "CHASSIS",
        "title": "Front Panel Audio & USB Headers",
        "plugs": "Plugs: Case Front USB 2.0/3.2 and HD Audio cables",
        "box": (30, 665, 350, 54),
        "anchor": (740, 810),
        "path": [(380, 692), (430, 692), (430, 810), (740, 810)],
    },
    # Right 1: DDR5 RAM Slots
    {
        "category": "COMPUTE",
        "title": "DDR5 Memory Slots (DIMM 1-4)",
        "plugs": "Plugs: System RAM sticks (Dual-Channel Priority A2/B2)",
        "box": (1480, 85, 350, 54),
        "anchor": (1020, 350),
        "path": [(1480, 112), (1390, 112), (1390, 350), (1020, 350)],
    },
    # Right 2: 24-Pin ATX Main Power Header
    {
        "category": "POWER",
        "title": "24-Pin ATX Main Power Header",
        "plugs": "Plugs: Main 24-Pin harness from PSU (powers board & chipset)",
        "box": (1480, 225, 350, 54),
        "anchor": (1250, 430),
        "path": [(1480, 252), (1350, 252), (1350, 430), (1250, 430)],
    },
    # Right 3: M.2 NVMe SSD Slot (Gen 5)
    {
        "category": "STORAGE",
        "title": "M.2 NVMe PCIe SSD Slot (Gen 5)",
        "plugs": "Plugs: High-speed M.2 2280 NVMe SSD (under heatsink)",
        "box": (1480, 365, 350, 54),
        "anchor": (890, 615),
        "path": [(1480, 392), (1320, 392), (1320, 615), (890, 615)],
    },
    # Right 4: Primary PCIe 5.0 x16 Slot
    {
        "category": "GPU",
        "title": "PCIe 5.0 x16 Slot (Steel Armor)",
        "plugs": "Plugs: Dedicated Graphics Card (Discrete GPU)",
        "box": (1480, 505, 350, 54),
        "anchor": (840, 695),
        "path": [(1480, 532), (1290, 532), (1290, 695), (840, 695)],
    },
    # Right 5: SATA 6Gbps Storage Ports
    {
        "category": "STORAGE",
        "title": "SATA 6Gbps Storage Ports",
        "plugs": "Plugs: SATA Data cables to 2.5\" SSDs & 3.5\" Hard Drives",
        "box": (1480, 645, 350, 54),
        "anchor": (1250, 710),
        "path": [(1480, 672), (1350, 672), (1350, 710), (1250, 710)],
    },
    # Bottom Right: Front Panel System Header
    {
        "category": "CHASSIS",
        "title": "Front Panel Switch/LED Header",
        "plugs": "Plugs: Case Power Switch, Reset Button, HDD & Power LEDs",
        "box": (1480, 785, 350, 54),
        "anchor": (1200, 780),
        "path": [(1480, 812), (1380, 812), (1380, 780), (1200, 780)],
    },
]

def draw_badge(draw, c, box):
    x, y, w, h = box
    col = COLORS[c["category"]]

    # Dark background pill with soft rounded corners
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=col["bg"], outline=col["border"], width=1)

    # Category tag pill
    cat_text = c["category"]
    cat_w = draw.textlength(cat_text, font=font_badge)
    tag_x = x + 12
    tag_y = y + 8
    draw.rounded_rectangle([tag_x, tag_y, tag_x + cat_w + 10, tag_y + 15], radius=3, fill=col["border"])
    draw.text((tag_x + 5, tag_y + 1), cat_text, fill=(11, 17, 32), font=font_badge)

    # Title text
    title_x = tag_x + cat_w + 16
    draw.text((title_x, y + 7), c["title"], fill=(248, 250, 252), font=font_title)

    # Subtitle / Plugs text
    draw.text((x + 14, y + 31), c["plugs"], fill=(203, 213, 225), font=font_subtitle)

def draw_trace(draw, c):
    col = COLORS[c["category"]]
    points = c["path"]
    ax, ay = c["anchor"]

    # Glow line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["glow"], width=5)

    # Sharp trace line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["border"], width=2)

    # Target anchor ring directly on the physical hardware port
    draw.ellipse([ax - 10, ay - 10, ax + 10, ay + 10], fill=col["glow"])
    draw.ellipse([ax - 6, ay - 6, ax + 6, ay + 6], fill=col["border"], outline=(255, 255, 255, 255), width=2)
    draw.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=(255, 255, 255, 255))

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
print(f"Successfully generated diagram with exact calibrated traces to {output_path}")
