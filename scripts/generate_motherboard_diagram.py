import os
from PIL import Image, ImageDraw, ImageFont

# Load base photograph
src_path = "public/images/hardware/motherboard-atx-landmarks.jpg"
img = Image.open(src_path).convert("RGBA")
W, H = img.size

# Overlay layer for lines and badges
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Fonts
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14)
font_subtitle = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 10)
font_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_subhdr = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)

# Subsystem color tokens (HSL-tailored, high contrast, dark mode compatible)
COLORS = {
    "COMPUTE":  {"border": (56, 189, 248, 255), "bg": (14, 34, 56, 240),  "accent": (56, 189, 248, 255), "glow": (56, 189, 248, 80)},
    "POWER":    {"border": (251, 191, 36, 255), "bg": (45, 33, 10, 240),  "accent": (251, 191, 36, 255), "glow": (251, 191, 36, 80)},
    "GPU":      {"border": (192, 132, 252, 255), "bg": (38, 20, 56, 240), "accent": (192, 132, 252, 255), "glow": (192, 132, 252, 80)},
    "STORAGE":  {"border": (52, 211, 153, 255), "bg": (12, 43, 30, 240),  "accent": (52, 211, 153, 255), "glow": (52, 211, 153, 80)},
    "IO":       {"border": (244, 63, 94, 255),  "bg": (50, 15, 26, 240),  "accent": (244, 63, 94, 255), "glow": (244, 63, 94, 80)},
    "EXPANSION":{"border": (129, 140, 248, 255), "bg": (25, 28, 60, 240), "accent": (129, 140, 248, 255), "glow": (129, 140, 248, 80)},
    "CHASSIS":  {"border": (148, 163, 184, 255), "bg": (25, 32, 44, 240), "accent": (148, 163, 184, 255), "glow": (148, 163, 184, 80)},
}

# Define callouts:
# anchor: point on the physical port (x, y)
# box: (x, y, w, h)
# side: 'left' or 'right' or 'top' for leader line connection
callouts = [
    # Top Left: CPU EPS Power
    {
        "category": "POWER",
        "title": "8+8 Pin CPU Power (EPS 12V)",
        "plugs": "Plugs: Dedicated PSU CPU power cables",
        "anchor": (380, 115),
        "box": (30, 20, 310, 52),
        "attach": "right",
    },
    # Top Center: CPU Socket
    {
        "category": "COMPUTE",
        "title": "CPU Socket (LGA 1700)",
        "plugs": "Plugs: Intel Core Processor (12th-14th Gen)",
        "anchor": (515, 410),
        "box": (420, 20, 330, 52),
        "attach": "bottom",
    },
    # Left 1: Rear I/O Panel
    {
        "category": "IO",
        "title": "Rear I/O Shield & External Ports",
        "plugs": "Plugs: Monitors, USB, 2.5GbE LAN, Audio",
        "anchor": (255, 330),
        "box": (20, 180, 290, 52),
        "attach": "right",
    },
    # Left 2: PCIe Expansion Slots
    {
        "category": "EXPANSION",
        "title": "PCIe Expansion Slots (x1 / x4)",
        "plugs": "Plugs: Wi-Fi, 10GbE NICs, Sound, Capture Cards",
        "anchor": (440, 660),
        "box": (20, 470, 310, 52),
        "attach": "right",
    },
    # Left 3: Front Panel & Case Headers
    {
        "category": "CHASSIS",
        "title": "Front Panel & Internal USB Headers",
        "plugs": "Plugs: Case Power Button, Reset, Audio, Front USB",
        "anchor": (500, 720),
        "box": (20, 690, 330, 52),
        "attach": "right",
    },
    # Right 1: DDR5 RAM Slots
    {
        "category": "COMPUTE",
        "title": "DDR5 Memory Slots (DIMM 1-4)",
        "plugs": "Plugs: System RAM (Dual-Channel Priority A2/B2)",
        "anchor": (665, 320),
        "box": (860, 100, 350, 52),
        "attach": "left",
    },
    # Right 2: 24-Pin ATX Main Power
    {
        "category": "POWER",
        "title": "24-Pin ATX Main Power Header",
        "plugs": "Plugs: PSU Main Harness (Motherboard Power)",
        "anchor": (758, 410),
        "box": (860, 230, 340, 52),
        "attach": "left",
    },
    # Right 3: M.2 NVMe SSD Slot
    {
        "category": "STORAGE",
        "title": "M.2 NVMe SSD Slot (Direct CPU PCIe 5.0)",
        "plugs": "Plugs: High-Speed M.2 2280 NVMe SSD (under armor)",
        "anchor": (480, 530),
        "box": (860, 360, 360, 52),
        "attach": "left",
    },
    # Right 4: Primary PCIe 5.0 x16 Slot (GPU)
    {
        "category": "GPU",
        "title": "PCIe 5.0 x16 Slot (Steel Armor)",
        "plugs": "Plugs: Dedicated Graphics Card (Discrete GPU)",
        "anchor": (450, 600),
        "box": (860, 490, 340, 52),
        "attach": "left",
    },
    # Right 5: SATA 6Gbps Storage Ports
    {
        "category": "STORAGE",
        "title": "SATA 6Gbps Storage Ports",
        "plugs": "Plugs: 2.5\" SATA SSDs & 3.5\" Spinning Hard Drives",
        "anchor": (758, 680),
        "box": (860, 620, 360, 52),
        "attach": "left",
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
    tag_x = x + 10
    tag_y = y + 7
    draw.rounded_rectangle([tag_x, tag_y, tag_x + cat_w + 10, tag_y + 14], radius=3, fill=col["border"])
    draw.text((tag_x + 5, tag_y + 1), cat_text, fill=(15, 23, 42), font=font_badge)

    # Title text
    title_x = tag_x + cat_w + 18
    draw.text((title_x, y + 6), c["title"], fill=(248, 250, 252), font=font_title)

    # Subtitle / Plugs text
    draw.text((x + 12, y + 29), c["plugs"], fill=(203, 213, 225), font=font_subtitle)

def draw_leader_line(draw, c):
    col = COLORS[c["category"]]
    ax, ay = c["anchor"]
    bx, by, bw, bh = c["box"]
    attach = c["attach"]

    if attach == "right":
        cx = bx + bw
        cy = by + bh // 2
        # Bend line
        mid_x = cx + (ax - cx) // 2
        points = [(cx, cy), (mid_x, cy), (mid_x, ay), (ax, ay)]
    elif attach == "left":
        cx = bx
        cy = by + bh // 2
        mid_x = cx - (cx - ax) // 2
        points = [(cx, cy), (mid_x, cy), (mid_x, ay), (ax, ay)]
    elif attach == "bottom":
        cx = bx + bw // 2
        cy = by + bh
        points = [(cx, cy), (cx, ay - 30), (ax, ay)]
    else:
        cx = bx + bw // 2
        cy = by
        points = [(cx, cy), (ax, ay)]

    # Draw glow line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["glow"], width=4)

    # Draw sharp leader line
    for p1, p2 in zip(points[:-1], points[1:]):
        draw.line([p1, p2], fill=col["border"], width=2)

    # Anchor point target ring
    draw.ellipse([ax - 9, ay - 9, ax + 9, ay + 9], fill=col["glow"])
    draw.ellipse([ax - 6, ay - 6, ax + 6, ay + 6], fill=col["border"], outline=(255, 255, 255, 255), width=2)
    draw.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=(255, 255, 255, 255))

# Draw all leader lines first (behind badges)
for c in callouts:
    draw_leader_line(draw, c)

# Draw all badges
for c in callouts:
    draw_badge(draw, c, c["box"])

# Composite
final_img = Image.alpha_composite(img, overlay).convert("RGB")
output_path = "public/images/hardware/motherboard-atx-landmarks.jpg"
final_img.save(output_path, quality=95)
print(f"Successfully generated labeled motherboard diagram to {output_path}")
