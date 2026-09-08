import os
from PIL import Image, ImageDraw, ImageFont

src_path = "original_motherboard.jpg"
base = Image.open(src_path).convert("RGBA")

CANVAS_W = 2600
CANVAS_H = 1200

OFFSET_X = 612
OFFSET_Y = 180

canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (10, 15, 29, 255))
canvas.paste(base, (OFFSET_X, OFFSET_Y))

overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# High-legibility large typography
font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38)
font_subhdr = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 21)
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 23)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)

# High-contrast color tokens
COLORS = {
    "COMPUTE":  {"border": (56, 189, 248, 255), "bg": (14, 30, 52, 250),  "accent": (56, 189, 248, 255), "glow": (56, 189, 248, 80)},
    "POWER":    {"border": (251, 191, 36, 255), "bg": (42, 30, 10, 250),  "accent": (251, 191, 36, 255), "glow": (251, 191, 36, 80)},
    "GPU":      {"border": (192, 132, 252, 255), "bg": (36, 18, 54, 250), "accent": (192, 132, 252, 255), "glow": (192, 132, 252, 80)},
    "STORAGE":  {"border": (52, 211, 153, 255), "bg": (12, 40, 28, 250),  "accent": (52, 211, 153, 255), "glow": (52, 211, 153, 80)},
    "IO":       {"border": (244, 63, 94, 255),  "bg": (48, 14, 25, 250),  "accent": (244, 63, 94, 255), "glow": (244, 63, 94, 80)},
    "EXPANSION":{"border": (129, 140, 248, 255), "bg": (22, 25, 58, 250), "accent": (129, 140, 248, 255), "glow": (129, 140, 248, 80)},
    "CHASSIS":  {"border": (148, 163, 184, 255), "bg": (26, 32, 44, 250), "accent": (148, 163, 184, 255), "glow": (148, 163, 184, 80)},
}

# Header banner at top
draw.text((45, 35), "ATX MOTHERBOARD INTERFACE & HARDWARE LANDMARK MAP", fill=(248, 250, 252), font=font_header)
draw.text((48, 85), "CompTIA A+ Core 1 physical reference: identifying where each subsystem connects to the system board.", fill=(148, 163, 184), font=font_subhdr)

def b2c(bx, by):
    return (bx + OFFSET_X, by + OFFSET_Y)

BOX_W = 540
BOX_H = 92
LEFT_X = 35
RIGHT_X = 2025

# Physical anchors verified on original photo:
# CPU EPS: (545, 112)
# Rear I/O: (260, 370)
# CPU Socket: (705, 335)
# M.2 NVMe: (620, 540)
# PCIe 5.0 x16 (GPU): (540, 612)
# Front Audio: (345, 715)
# DDR5 RAM: (910, 360)
# 24-Pin ATX: (1050, 408)
# SATA 6Gbps: (1045, 655)
# Front Panel: (995, 732)

callouts = [
    # LEFT COLUMN (6 items) — all components situated on the left/center of board
    # L1: CPU EPS Power (Y=130)
    {
        "category": "POWER",
        "title": "8+8 Pin CPU Power (EPS 12V)",
        "plugs": "Plugs: Dedicated 8-Pin CPU 12V power cables from PSU",
        "box": (LEFT_X, 130, BOX_W, BOX_H),
        "anchor": b2c(545, 112),
        "path": [(LEFT_X + BOX_W, 176), (b2c(545, 112)[0], 176), b2c(545, 112)],
    },
    # L2: Rear I/O External Ports (Y=295)
    {
        "category": "IO",
        "title": "Rear I/O External Ports",
        "plugs": "Plugs: Monitors (DP/HDMI), 2.5GbE LAN, USB, Audio",
        "box": (LEFT_X, 295, BOX_W, BOX_H),
        "anchor": b2c(260, 370),
        "path": [(LEFT_X + BOX_W, 341), (b2c(260, 370)[0] - 80, 341), (b2c(260, 370)[0] - 80, b2c(260, 370)[1]), b2c(260, 370)],
    },
    # L3: CPU Socket LGA 1700 (Y=460)
    {
        "category": "COMPUTE",
        "title": "CPU Socket (LGA 1700)",
        "plugs": "Plugs: Processor (Intel Core 12th-14th Gen) under ZIF lever",
        "box": (LEFT_X, 460, BOX_W, BOX_H),
        "anchor": b2c(705, 335),
        "path": [(LEFT_X + BOX_W, 506), (b2c(705, 335)[0] - 130, 506), (b2c(705, 335)[0] - 130, b2c(705, 335)[1]), b2c(705, 335)],
    },
    # L4: M.2 NVMe PCIe SSD Slot (Y=625)
    {
        "category": "STORAGE",
        "title": "M.2 NVMe PCIe SSD Slot (Gen 5)",
        "plugs": "Plugs: High-speed M.2 2280 NVMe SSD (under heatsink)",
        "box": (LEFT_X, 625, BOX_W, BOX_H),
        "anchor": b2c(620, 540),
        "path": [(LEFT_X + BOX_W, 671), (b2c(620, 540)[0] - 150, 671), (b2c(620, 540)[0] - 150, b2c(620, 540)[1]), b2c(620, 540)],
    },
    # L5: Primary PCIe 5.0 x16 Slot (GPU) (Y=790)
    {
        "category": "GPU",
        "title": "PCIe 5.0 x16 Slot (Steel Armor)",
        "plugs": "Plugs: Dedicated Graphics Card (Discrete GPU)",
        "box": (LEFT_X, 790, BOX_W, BOX_H),
        "anchor": b2c(540, 612),
        "path": [(LEFT_X + BOX_W, 836), (b2c(540, 612)[0] - 100, 836), (b2c(540, 612)[0] - 100, b2c(540, 612)[1]), b2c(540, 612)],
    },
    # L6: Front Panel Audio & USB Headers (Y=955)
    {
        "category": "CHASSIS",
        "title": "Front Panel Audio & USB Headers",
        "plugs": "Plugs: Case Front USB 2.0/3.2 and HD Audio cables",
        "box": (LEFT_X, 955, BOX_W, BOX_H),
        "anchor": b2c(345, 715),
        "path": [(LEFT_X + BOX_W, 1001), (b2c(345, 715)[0] - 50, 1001), (b2c(345, 715)[0] - 50, b2c(345, 715)[1]), b2c(345, 715)],
    },

    # RIGHT COLUMN (4 items) — all components situated on the right of board
    # R1: DDR5 RAM Slots (Y=180)
    {
        "category": "COMPUTE",
        "title": "DDR5 Memory Slots (DIMM 1-4)",
        "plugs": "Plugs: System RAM sticks (Dual-Channel Priority A2/B2)",
        "box": (RIGHT_X, 180, BOX_W, BOX_H),
        "anchor": b2c(910, 360),
        "path": [(RIGHT_X, 226), (b2c(910, 360)[0] + 60, 226), (b2c(910, 360)[0] + 60, b2c(910, 360)[1]), b2c(910, 360)],
    },
    # R2: 24-Pin ATX Main Power Header (Y=390)
    {
        "category": "POWER",
        "title": "24-Pin ATX Main Power Header",
        "plugs": "Plugs: Main 24-Pin harness from PSU (powers board & chipset)",
        "box": (RIGHT_X, 390, BOX_W, BOX_H),
        "anchor": b2c(1050, 408),
        "path": [(RIGHT_X, 436), (b2c(1050, 408)[0] + 70, 436), (b2c(1050, 408)[0] + 70, b2c(1050, 408)[1]), b2c(1050, 408)],
    },
    # R3: SATA 6Gbps Storage Ports (Y=650)
    {
        "category": "STORAGE",
        "title": "SATA 6Gbps Storage Ports",
        "plugs": "Plugs: SATA Data cables to 2.5\" SSDs & 3.5\" Hard Drives",
        "box": (RIGHT_X, 650, BOX_W, BOX_H),
        "anchor": b2c(1045, 655),
        "path": [(RIGHT_X, 696), (b2c(1045, 655)[0] + 70, 696), (b2c(1045, 655)[0] + 70, b2c(1045, 655)[1]), b2c(1045, 655)],
    },
    # R4: Front Panel Switch/LED Header (Y=880)
    {
        "category": "CHASSIS",
        "title": "Front Panel Switch/LED Header",
        "plugs": "Plugs: Case Power Switch, Reset Button, HDD & Power LEDs",
        "box": (RIGHT_X, 880, BOX_W, BOX_H),
        "anchor": b2c(995, 732),
        "path": [(RIGHT_X, 926), (b2c(995, 732)[0] + 80, 926), (b2c(995, 732)[0] + 80, b2c(995, 732)[1]), b2c(995, 732)],
    },
]

def draw_badge(draw, c, box):
    x, y, w, h = box
    col = COLORS[c["category"]]

    # Dark background box with rounded corners
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=col["bg"], outline=col["border"], width=2)

    # Category tag pill
    cat_text = c["category"]
    cat_w = draw.textlength(cat_text, font=font_badge)
    tag_x = x + 16
    tag_y = y + 14
    tag_h = 24
    draw.rounded_rectangle([tag_x, tag_y, tag_x + cat_w + 16, tag_y + tag_h], radius=6, fill=col["border"])
    draw.text((tag_x + 8, tag_y + 3), cat_text, fill=(10, 15, 29), font=font_badge)

    # Title text (large 23px bold)
    title_x = tag_x + cat_w + 22
    draw.text((title_x, y + 13), c["title"], fill=(248, 250, 252), font=font_title)

    # Subtitle / Plugs text (18px clean)
    draw.text((x + 18, y + 52), c["plugs"], fill=(203, 213, 225), font=font_subtitle)

def draw_trace(draw, c):
    col = COLORS[c["category"]]
    points = c["path"]
    ax, ay = c["anchor"]

    # Wide glow line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["glow"], width=8)

    # Sharp trace line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["border"], width=3)

    # Target anchor ring directly on the physical hardware port
    draw.ellipse([ax - 14, ay - 14, ax + 14, ay + 14], fill=col["glow"])
    draw.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=col["border"], outline=(255, 255, 255, 255), width=2)
    draw.ellipse([ax - 4, ay - 4, ax + 4, ay + 4], fill=(255, 255, 255, 255))

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
print(f"Successfully generated clean natural-flow diagram ({CANVAS_W}x{CANVAS_H}) to {output_path}")
