import os
from PIL import Image, ImageDraw, ImageFont

# Load original base photograph
src_path = "original_motherboard.jpg"
base = Image.open(src_path).convert("RGBA")
base_w, base_h = base.size

# Target canvas: 1860 x 940 gives generous margins on all 4 sides
CANVAS_W = 1860
CANVAS_H = 940

# Offset to center the base image in the canvas
OFFSET_X = 240
OFFSET_Y = 85

# Create canvas with sleek dark background matching LMS theme (#0b1120)
canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (11, 17, 32, 255))

# Paste base motherboard image in center
canvas.paste(base, (OFFSET_X, OFFSET_Y))

# Create drawing layer for lines and badges
overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Fonts
font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_subhdr = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 9)

# Colors tailored for high contrast and pedagogical clarity
COLORS = {
    "COMPUTE":  {"border": (56, 189, 248, 255), "bg": (14, 30, 50, 248),  "accent": (56, 189, 248, 255), "glow": (56, 189, 248, 90)},
    "POWER":    {"border": (251, 191, 36, 255), "bg": (40, 30, 10, 248),  "accent": (251, 191, 36, 255), "glow": (251, 191, 36, 90)},
    "GPU":      {"border": (192, 132, 252, 255), "bg": (35, 18, 52, 248), "accent": (192, 132, 252, 255), "glow": (192, 132, 252, 90)},
    "STORAGE":  {"border": (52, 211, 153, 255), "bg": (12, 38, 28, 248),  "accent": (52, 211, 153, 255), "glow": (52, 211, 153, 90)},
    "IO":       {"border": (244, 63, 94, 255),  "bg": (45, 14, 24, 248),  "accent": (244, 63, 94, 255), "glow": (244, 63, 94, 90)},
    "EXPANSION":{"border": (129, 140, 248, 255), "bg": (22, 25, 55, 248), "accent": (129, 140, 248, 255), "glow": (129, 140, 248, 90)},
    "CHASSIS":  {"border": (148, 163, 184, 255), "bg": (24, 30, 42, 248), "accent": (148, 163, 184, 255), "glow": (148, 163, 184, 90)},
}

# Header banner at top
draw.text((30, 18), "ATX MOTHERBOARD INTERFACE & HARDWARE LANDMARK MAP", fill=(248, 250, 252), font=font_header)
draw.text((32, 45), "CompTIA A+ Core 1 physical reference: identifying where each subsystem connects to the system board.", fill=(148, 163, 184), font=font_subhdr)

# Helper to transform board coords to canvas coords
def to_canvas(bx, by):
    return (bx + OFFSET_X, by + OFFSET_Y)

# Calibrated callouts
callouts = [
    # Top Left: CPU EPS Power
    {
        "category": "POWER",
        "title": "8+8 Pin CPU Power (EPS 12V)",
        "plugs": "Plugs: Dedicated 8-Pin CPU 12V power cables from PSU",
        "anchor": to_canvas(580, 110),
        "box": (30, 85, 350, 54),
        "side": "right",
    },
    # Top Center: CPU Socket
    {
        "category": "COMPUTE",
        "title": "CPU Socket (LGA 1700)",
        "plugs": "Plugs: Processor (Intel Core 12th-14th Gen) under ZIF lever",
        "anchor": to_canvas(710, 370),
        "box": (800, 16, 380, 54),
        "side": "top_center",
    },
    # Left 2: Rear I/O Panel
    {
        "category": "IO",
        "title": "Rear I/O External Ports",
        "plugs": "Plugs: Monitors (DP/HDMI), 2.5GbE LAN, USB, Audio",
        "anchor": to_canvas(290, 330),
        "box": (30, 245, 350, 54),
        "side": "right",
    },
    # Left 3: PCIe Expansion Slots
    {
        "category": "EXPANSION",
        "title": "PCIe Expansion Slots (x1 / x4)",
        "plugs": "Plugs: Add-in cards (Wi-Fi, 10GbE NICs, Sound, Capture)",
        "anchor": to_canvas(490, 690),
        "box": (30, 440, 350, 54),
        "side": "right",
    },
    # Left 4: Front Audio & Case Headers
    {
        "category": "CHASSIS",
        "title": "Front Panel Audio & USB Headers",
        "plugs": "Plugs: Case Front USB 2.0/3.2 and HD Audio cables",
        "anchor": to_canvas(500, 725),
        "box": (30, 665, 350, 54),
        "side": "right",
    },
    # Right 1: DDR5 RAM Slots
    {
        "category": "COMPUTE",
        "title": "DDR5 Memory Slots (DIMM 1-4)",
        "plugs": "Plugs: System RAM sticks (Dual-Channel Priority A2/B2)",
        "anchor": to_canvas(980, 350),
        "box": (1480, 85, 350, 54),
        "side": "left",
    },
    # Right 2: 24-Pin ATX Power
    {
        "category": "POWER",
        "title": "24-Pin ATX Main Power Header",
        "plugs": "Plugs: Main 24-Pin harness from PSU (powers board & chipset)",
        "anchor": to_canvas(1170, 360),
        "box": (1480, 225, 350, 54),
        "side": "left",
    },
    # Right 3: M.2 NVMe SSD Slot
    {
        "category": "STORAGE",
        "title": "M.2 NVMe PCIe SSD Slot (Gen 5)",
        "plugs": "Plugs: High-speed M.2 2280 NVMe SSD (under heatsink)",
        "anchor": to_canvas(650, 535),
        "box": (1480, 365, 350, 54),
        "side": "left",
    },
    # Right 4: Primary PCIe 5.0 x16 Slot
    {
        "category": "GPU",
        "title": "PCIe 5.0 x16 Slot (Steel Armor)",
        "plugs": "Plugs: Dedicated Graphics Card (Discrete GPU)",
        "anchor": to_canvas(660, 610),
        "box": (1480, 505, 350, 54),
        "side": "left",
    },
    # Right 5: SATA 6Gbps Ports
    {
        "category": "STORAGE",
        "title": "SATA 6Gbps Storage Ports",
        "plugs": "Plugs: SATA Data cables to 2.5\" SSDs & 3.5\" Hard Drives",
        "anchor": to_canvas(1185, 665),
        "box": (1480, 645, 350, 54),
        "side": "left",
    },
    # Bottom Right: Front Panel System Header
    {
        "category": "CHASSIS",
        "title": "Front Panel Switch/LED Header",
        "plugs": "Plugs: Case Power Switch, Reset Button, HDD & Power LEDs",
        "anchor": to_canvas(1045, 712),
        "box": (1480, 785, 350, 54),
        "side": "left",
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

def draw_leader_line(draw, c):
    col = COLORS[c["category"]]
    ax, ay = c["anchor"]
    bx, by, bw, bh = c["box"]
    side = c["side"]

    if side == "right":
        cx = bx + bw
        cy = by + bh // 2
        mid_x = cx + (ax - cx) // 2
        points = [(cx, cy), (mid_x, cy), (mid_x, ay), (ax, ay)]
    elif side == "left":
        cx = bx
        cy = by + bh // 2
        mid_x = cx - (cx - ax) // 2
        points = [(cx, cy), (mid_x, cy), (mid_x, ay), (ax, ay)]
    elif side == "top_center":
        cx = bx + bw // 2
        cy = by + bh
        points = [(cx, cy), (cx, ay - 40), (ax, ay)]
    else:
        cx = bx + bw // 2
        cy = by
        points = [(cx, cy), (ax, ay)]

    # Draw glow line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["glow"], width=5)

    # Draw crisp leader line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["border"], width=2)

    # Anchor point target ring
    draw.ellipse([ax - 10, ay - 10, ax + 10, ay + 10], fill=col["glow"])
    draw.ellipse([ax - 6, ay - 6, ax + 6, ay + 6], fill=col["border"], outline=(255, 255, 255, 255), width=2)
    draw.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=(255, 255, 255, 255))

# Draw all leader lines
for c in callouts:
    draw_leader_line(draw, c)

# Draw all badges
for c in callouts:
    draw_badge(draw, c, c["box"])

# Composite overlay on top of canvas
final_img = Image.alpha_composite(canvas, overlay).convert("RGB")
output_path = "public/images/hardware/motherboard-atx-landmarks.jpg"
final_img.save(output_path, quality=95)
print(f"Successfully generated diagram to {output_path}")
