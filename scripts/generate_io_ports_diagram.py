import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    return {
        "header": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 40),
        "subhdr": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 21),
        "card_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22),
        "badge": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13),
        "speed_badge": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14),
        "body_bold": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16),
        "body": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16),
        "tip": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18),
    }

def draw_port_card(draw, fonts, x, y, w, h, title, category, speed, items, col):
    # Card background
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=col["bg"], outline=col["border"], width=2)

    # Category Pill
    cat_w = draw.textlength(category, font=fonts["badge"])
    draw.rounded_rectangle([x + 18, y + 16, x + 18 + cat_w + 14, y + 16 + 22], radius=5, fill=col["accent"])
    draw.text((x + 25, y + 18), category, fill=(10, 15, 29), font=fonts["badge"])

    # Speed Pill (Right aligned)
    sp_w = draw.textlength(speed, font=fonts["speed_badge"])
    draw.rounded_rectangle([x + w - sp_w - 30, y + 16, x + w - 16, y + 16 + 22], radius=5, fill=(255, 255, 255, 20), outline=col["border"], width=1)
    draw.text((x + w - sp_w - 23, y + 18), speed, fill=col["accent"], font=fonts["speed_badge"])

    # Title
    draw.text((x + 18, y + 48), title, fill=(248, 250, 252), font=fonts["card_title"])

    # Divider
    draw.line([(x + 18, y + 82), (x + w - 18, y + 82)], fill=(255, 255, 255, 30), width=1)

    # Bullet points
    curr_y = y + 96
    for label, desc in items:
        draw.ellipse([x + 20, curr_y + 5, x + 26, curr_y + 11], fill=col["accent"])
        draw.text((x + 34, curr_y), label, fill=(241, 245, 249), font=fonts["body_bold"])
        l_len = draw.textlength(label + " ", font=fonts["body_bold"])
        draw.text((x + 34 + l_len, curr_y), desc, fill=(203, 213, 225), font=fonts["body"])
        curr_y += 30

def generate_io_diagram(out_path):
    W, H = 2500, 1380
    img = Image.new("RGBA", (W, H), (10, 15, 29, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fonts = get_fonts()

    # Header
    draw.text((60, 40), "COMMON PERIPHERAL PORTS, CABLES & SIGNALING PROTOCOLS", fill=(248, 250, 252), font=fonts["header"])
    draw.text((64, 96), "CompTIA Tech+ FC0-U71 physical interface identification, pinout configurations, and maximum throughput specs", fill=(148, 163, 184), font=fonts["subhdr"])

    # Palettes
    c_blue = {"bg": (14, 28, 48, 250), "border": (56, 189, 248, 255), "accent": (56, 189, 248, 255)}
    c_amber = {"bg": (36, 26, 12, 250), "border": (251, 191, 36, 255), "accent": (251, 191, 36, 255)}
    c_purple = {"bg": (32, 18, 50, 250), "border": (192, 132, 252, 255), "accent": (192, 132, 252, 255)}
    c_green = {"bg": (12, 38, 26, 250), "border": (52, 211, 153, 255), "accent": (52, 211, 153, 255)}
    c_rose = {"bg": (38, 14, 24, 250), "border": (244, 63, 94, 255), "accent": (244, 63, 94, 255)}
    c_indigo = {"bg": (20, 24, 56, 250), "border": (129, 140, 248, 255), "accent": (129, 140, 248, 255)}
    c_orange = {"bg": (42, 22, 10, 250), "border": (251, 146, 60, 255), "accent": (251, 146, 60, 255)}
    c_slate = {"bg": (22, 30, 44, 250), "border": (148, 163, 184, 255), "accent": (148, 163, 184, 255)}

    CARD_W = 565
    CARD_H = 345
    ROW1_Y = 160
    ROW2_Y = 540
    ROW3_Y = 920

    # 6 Major Cards (2 rows of 3)
    # Card 1: USB Type-A
    c1_items = [
        ("Physical Shape:", "Rectangular, keyed to insert only one way."),
        ("Pin Count:", "4 pins (USB 2.0 black) / 9 pins (USB 3.0 blue)."),
        ("Signaling:", "USB 2.0 (480 Mbps) vs USB 3.2 Gen 1 (5 Gbps)."),
        ("Primary Use:", "Mice, keyboards, flash drives, legacy printers."),
        ("Exam Trap:", "Blue plastic insert denotes SuperSpeed 5Gbps+."),
    ]
    draw_port_card(draw, fonts, 60, ROW1_Y, 740, 340, "USB Type-A (Standard USB)", "UNIVERSAL BUS", "Up to 10 Gbps", c1_items, c_blue)

    # Card 2: USB Type-C & Thunderbolt
    c2_items = [
        ("Physical Shape:", "Slim oval, fully symmetrical & reversible."),
        ("Pin Count:", "24 pins with high-density differential pairs."),
        ("Signaling:", "USB 3.2, USB4, and Thunderbolt 3/4 (up to 40 Gbps)."),
        ("Alt-Mode:", "Transmits native DisplayPort video & 240W USB-PD power."),
        ("Identification:", "Thunderbolt ports feature a lightning bolt symbol."),
    ]
    draw_port_card(draw, fonts, 880, ROW1_Y, 740, 340, "USB Type-C & Thunderbolt 3/4", "HIGH-SPEED / VIDEO", "Up to 40 Gbps", c2_items, c_purple)

    # Card 3: RJ-45 Ethernet (vs RJ-11)
    c3_items = [
        ("Physical Shape:", "8P8C modular plastic plug with retention snap latch."),
        ("Pin Count:", "8 copper pins connecting 4 twisted pairs (UTP/STP)."),
        ("Throughput:", "1 Gbps (Cat 5e/6) to 10 Gbps (Cat 6a) up to 100 meters."),
        ("Phone Diff:", "RJ-11 phone cable has only 4 or 6 pins and is narrower."),
        ("Exam Trap:", "Never force RJ-11 into RJ-45; pins 1 and 8 will bend."),
    ]
    draw_port_card(draw, fonts, 1700, ROW1_Y, 740, 340, "RJ-45 Ethernet (8P8C)", "NETWORK CABLE", "1 Gbps - 10 Gbps", c3_items, c_green)

    # Card 4: HDMI (High-Definition Multimedia)
    c4_items = [
        ("Physical Shape:", "Trapezoidal 19-pin connector with two notched corners."),
        ("Payload:", "Uncompressed digital video + multi-channel digital audio."),
        ("Standards:", "HDMI 2.0 (18 Gbps / 4K 60Hz), HDMI 2.1 (48 Gbps / 8K)."),
        ("Features:", "Audio Return Channel (ARC/eARC), HDCP copy protection."),
        ("Primary Use:", "TVs, monitors, projectors, gaming consoles."),
    ]
    draw_port_card(draw, fonts, 60, ROW2_Y + 20, 740, 340, "HDMI (High-Definition Multimedia)", "AUDIO / VIDEO", "Up to 48 Gbps", c4_items, c_rose)

    # Card 5: DisplayPort (DP)
    c5_items = [
        ("Physical Shape:", "Rectangular with ONE angled corner & mechanical latch."),
        ("Security:", "Built-in locking hooks (must press release button to pull)."),
        ("Throughput:", "DP 1.4 (32.4 Gbps / 4K 144Hz) to DP 2.1 (80 Gbps / 16K)."),
        ("Key Feature:", "Multi-Stream Transport (MST) enables monitor daisy-chaining."),
        ("Primary Use:", "High-refresh PC gaming monitors and workstation GPUs."),
    ]
    draw_port_card(draw, fonts, 880, ROW2_Y + 20, 740, 340, "DisplayPort (DP 1.4 / 2.1)", "PC DISPLAY", "Up to 80 Gbps", c5_items, c_amber)

    # Card 6: 3.5mm Audio & Legacy Video (VGA / DVI)
    c6_items = [
        ("3.5mm Jack:", "TRS (stereo output) vs TRRS (stereo audio + microphone)."),
        ("VGA (DE-15):", "Blue 15-pin connector, ANALOG ONLY, max 1080p, thumb-screws."),
        ("DVI Standards:", "DVI-D (digital only), DVI-A (analog only), DVI-I (integrated)."),
        ("Audio Gap:", "VGA and standard DVI carry NO AUDIO — separate cable required."),
        ("Converter Trap:", "VGA to HDMI requires active analog-to-digital DAC converter."),
    ]
    draw_port_card(draw, fonts, 1700, ROW2_Y + 20, 740, 340, "Audio & Legacy Display (VGA/DVI)", "ANALOG / HYBRID", "Legacy Standards", c6_items, c_slate)

    # Comparison Quick Reference Banner at bottom
    draw.rounded_rectangle([60, 960, 2440, 1260], radius=14, fill=(16, 22, 36), outline=(56, 189, 248, 120), width=2)

    draw.text((90, 985), "QUICK PHYSICAL IDENTIFICATION & EXAM CHEAT-SHEET", fill=(56, 189, 248), font=fonts["card_title"])

    draw.line([(90, 1020), (2410, 1020)], fill=(255, 255, 255, 25), width=1)

    col_w = 560
    # Col A: Video Latching
    draw.text((90, 1035), "DISPLAYPORT vs HDMI LATCHING", fill=(251, 191, 36), font=fonts["body_bold"])
    draw.text((90, 1065), "DisplayPort cables have mechanical latches with a release", fill=(203, 213, 225), font=fonts["body"])
    draw.text((90, 1095), "button. Pulling a DP cable without pressing the release", fill=(203, 213, 225), font=fonts["body"])
    draw.text((90, 1125), "button will tear the port off the graphics card solder pads.", fill=(248, 113, 113), font=fonts["body"])
    draw.text((90, 1155), "HDMI cables rely purely on friction and pull out freely.", fill=(148, 163, 184), font=fonts["body"])

    # Col B: USB Speeds
    draw.text((700, 1035), "USB COLOR CODE CONVENTION", fill=(56, 189, 248), font=fonts["body_bold"])
    draw.text((700, 1065), "• Black / White: USB 2.0 (HighSpeed, 480 Mbps)", fill=(203, 213, 225), font=fonts["body"])
    draw.text((700, 1095), "• Blue: USB 3.2 Gen 1 (SuperSpeed, 5 Gbps)", fill=(56, 189, 248), font=fonts["body"])
    draw.text((700, 1125), "• Teal / Red: USB 3.2 Gen 2 (SuperSpeed+, 10 Gbps)", fill=(244, 63, 94), font=fonts["body"])
    draw.text((700, 1155), "• Yellow / Orange: Always-On Power (Sleep & Charge)", fill=(251, 191, 36), font=fonts["body"])

    # Col C: Audio Rings
    draw.text((1310, 1035), "3.5MM AUDIO RING COUNT", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((1310, 1065), "• TS (1 Ring): Mono audio (guitars, microphones)", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1310, 1095), "• TRS (2 Rings): Stereo Left + Right headphones", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1310, 1125), "• TRRS (3 Rings): Stereo Audio + Inline Mic (headset)", fill=(192, 132, 252), font=fonts["body"])
    draw.text((1310, 1155), "Plugging TRS into TRRS port causes mic to not function.", fill=(248, 113, 113), font=fonts["body"])

    # Col D: Network Cable
    draw.text((1900, 1035), "RJ-45 vs RJ-11 MODULAR", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((1900, 1065), "• RJ-45: 8 pins, 4 pairs, Ethernet networks (LAN)", fill=(52, 211, 153), font=fonts["body"])
    draw.text((1900, 1095), "• RJ-11: 4/6 pins, 2 pairs, Analog telephone / DSL", fill=(148, 163, 184), font=fonts["body"])
    draw.text((1900, 1125), "• Cat 5e / Cat 6: Max channel length is 100 meters", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1900, 1155), "Always verify clip clicks securely into the port.", fill=(203, 213, 225), font=fonts["body"])

    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    final_img.save(out_path, quality=95)
    print(f"Generated I/O ports diagram to {out_path}")

if __name__ == "__main__":
    generate_io_diagram("public/images/tech-plus/io-ports-cables-guide.jpg")
