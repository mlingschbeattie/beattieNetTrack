import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    return {
        "header": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38),
        "subhdr": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 21),
        "drive_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 24),
        "badge": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14),
        "body_bold": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16),
        "body": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16),
        "callout_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20),
    }

def generate_storage_diagram(photo_src, out_path):
    W, H = 2500, 1350
    canvas = Image.new("RGBA", (W, H), (10, 15, 29, 255))

    # Load and scale photo to fit center-top
    photo = Image.open(photo_src).convert("RGBA")
    # Original is 1376 x 768. Let's scale up slightly to 1500 x 837 or keep 1440 x 803
    p_w = 1500
    p_h = int(photo.height * (p_w / photo.width))
    photo_scaled = photo.resize((p_w, p_h), Image.Resampling.LANCZOS)

    # Center photo horizontally
    px = (W - p_w) // 2
    py = 140
    canvas.paste(photo_scaled, (px, py))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fonts = get_fonts()

    # Header
    draw.text((60, 35), "STORAGE DRIVE FORM FACTORS, BUS INTERFACES & PERFORMANCE", fill=(248, 250, 252), font=fonts["header"])
    draw.text((64, 88), "CompTIA Tech+ FC0-U71 physical teardown: 3.5\" Mechanical HDD vs. 2.5\" SATA SSD vs. M.2 NVMe PCIe SSD", fill=(148, 163, 184), font=fonts["subhdr"])

    # Draw border around photo
    draw.rounded_rectangle([px - 4, py - 4, px + p_w + 4, py + p_h + 4], radius=12, fill=None, outline=(56, 189, 248, 120), width=2)

    # 3 Column Cards below photo
    c_hdd = {"bg": (28, 22, 16, 250), "border": (251, 146, 60, 255), "accent": (251, 146, 60, 255)}
    c_sata = {"bg": (14, 28, 48, 250), "border": (56, 189, 248, 255), "accent": (56, 189, 248, 255)}
    c_nvme = {"bg": (12, 38, 26, 250), "border": (52, 211, 153, 255), "accent": (52, 211, 153, 255)}

    CARD_W = 760
    CARD_H = 310
    CARD_Y = py + p_h + 24

    # Card 1: 3.5" Mechanical HDD (Left)
    c1_x = 60
    draw.rounded_rectangle([c1_x, CARD_Y, c1_x + CARD_W, CARD_Y + CARD_H], radius=14, fill=c_hdd["bg"], outline=c_hdd["border"], width=2)
    # Badge
    draw.rounded_rectangle([c1_x + 18, CARD_Y + 16, c1_x + 18 + 175, CARD_Y + 16 + 24], radius=6, fill=c_hdd["accent"])
    draw.text((c1_x + 26, CARD_Y + 18), "MAGNETIC MECHANICAL", fill=(10, 15, 29), font=fonts["badge"])
    # Speed pill
    draw.rounded_rectangle([c1_x + CARD_W - 170, CARD_Y + 16, c1_x + CARD_W - 18, CARD_Y + 16 + 24], radius=6, fill=(255, 255, 255, 20), outline=c_hdd["border"], width=1)
    draw.text((c1_x + CARD_W - 160, CARD_Y + 18), "120 - 220 MB/s", fill=c_hdd["accent"], font=fonts["badge"])

    draw.text((c1_x + 18, CARD_Y + 50), "3.5\" Mechanical Hard Disk Drive (HDD)", fill=(248, 250, 252), font=fonts["drive_title"])
    draw.line([(c1_x + 18, CARD_Y + 84), (c1_x + CARD_W - 18, CARD_Y + 84)], fill=(255, 255, 255, 30), width=1)

    hdd_bullets = [
        ("Physical Media:", "Aluminum/glass platters spinning at 5,400 or 7,200 RPM."),
        ("Moving Parts:", "Voice-coil actuator arm flies magnetic heads nanometers over platter."),
        ("Interface / Cable:", "Requires 7-pin SATA Data cable + 15-pin SATA Power cable."),
        ("Latency & Seek:", "High mechanical seek latency (8 to 15 ms). Vulnerable to drop shocks."),
        ("Best Use Case:", "Lowest cost-per-terabyte: ideal for NAS arrays, bulk video, & cold backups."),
    ]
    cy = CARD_Y + 98
    for lbl, txt in hdd_bullets:
        draw.ellipse([c1_x + 20, cy + 5, c1_x + 26, cy + 11], fill=c_hdd["accent"])
        draw.text((c1_x + 34, cy), lbl, fill=(241, 245, 249), font=fonts["body_bold"])
        l_len = draw.textlength(lbl + " ", font=fonts["body_bold"])
        draw.text((c1_x + 34 + l_len, cy), txt, fill=(203, 213, 225), font=fonts["body"])
        cy += 28

    # Card 2: 2.5" SATA SSD (Center)
    c2_x = 870
    draw.rounded_rectangle([c2_x, CARD_Y, c2_x + CARD_W, CARD_Y + CARD_H], radius=14, fill=c_sata["bg"], outline=c_sata["border"], width=2)
    # Badge
    draw.rounded_rectangle([c2_x + 18, CARD_Y + 16, c2_x + 18 + 155, CARD_Y + 16 + 24], radius=6, fill=c_sata["accent"])
    draw.text((c2_x + 26, CARD_Y + 18), "2.5\" SOLID-STATE", fill=(10, 15, 29), font=fonts["badge"])
    # Speed pill
    draw.rounded_rectangle([c2_x + CARD_W - 175, CARD_Y + 16, c2_x + CARD_W - 18, CARD_Y + 16 + 24], radius=6, fill=(255, 255, 255, 20), outline=c_sata["border"], width=1)
    draw.text((c2_x + CARD_W - 165, CARD_Y + 18), "Up to 550 MB/s", fill=c_sata["accent"], font=fonts["badge"])

    draw.text((c2_x + 18, CARD_Y + 50), "2.5\" SATA Solid-State Drive (SSD)", fill=(248, 250, 252), font=fonts["drive_title"])
    draw.line([(c2_x + 18, CARD_Y + 84), (c2_x + CARD_W - 18, CARD_Y + 84)], fill=(255, 255, 255, 30), width=1)

    sata_bullets = [
        ("Flash Media:", "Non-volatile 3D NAND flash memory cells + internal controller."),
        ("Durability:", "Zero moving parts — immune to vibration, drops, and head crashes."),
        ("Interface / Cable:", "Same 7-pin SATA Data + 15-pin SATA Power as mechanical HDD."),
        ("Bottleneck:", "Limited by SATA 3.0 interface ceiling (6 Gbps theoretical = ~550 MB/s real)."),
        ("Best Use Case:", "Drop-in speed upgrade for older laptops, desktops, and secondary SSD pools."),
    ]
    cy = CARD_Y + 98
    for lbl, txt in sata_bullets:
        draw.ellipse([c2_x + 20, cy + 5, c2_x + 26, cy + 11], fill=c_sata["accent"])
        draw.text((c2_x + 34, cy), lbl, fill=(241, 245, 249), font=fonts["body_bold"])
        l_len = draw.textlength(lbl + " ", font=fonts["body_bold"])
        draw.text((c2_x + 34 + l_len, cy), txt, fill=(203, 213, 225), font=fonts["body"])
        cy += 28

    # Card 3: M.2 NVMe PCIe SSD (Right)
    c3_x = 1680
    draw.rounded_rectangle([c3_x, CARD_Y, c3_x + CARD_W, CARD_Y + CARD_H], radius=14, fill=c_nvme["bg"], outline=c_nvme["border"], width=2)
    # Badge
    draw.rounded_rectangle([c3_x + 18, CARD_Y + 16, c3_x + 18 + 150, CARD_Y + 16 + 24], radius=6, fill=c_nvme["accent"])
    draw.text((c3_x + 26, CARD_Y + 18), "M.2 PCIE / NVME", fill=(10, 15, 29), font=fonts["badge"])
    # Speed pill
    draw.rounded_rectangle([c3_x + CARD_W - 195, CARD_Y + 16, c3_x + CARD_W - 18, CARD_Y + 16 + 24], radius=6, fill=(255, 255, 255, 20), outline=c_nvme["border"], width=1)
    draw.text((c3_x + CARD_W - 185, CARD_Y + 18), "3,500 - 7,500+ MB/s", fill=c_nvme["accent"], font=fonts["badge"])

    draw.text((c3_x + 18, CARD_Y + 50), "M.2 NVMe PCIe SSD (2280)", fill=(248, 250, 252), font=fonts["drive_title"])
    draw.line([(c3_x + 18, CARD_Y + 84), (c3_x + CARD_W - 18, CARD_Y + 84)], fill=(255, 255, 255, 30), width=1)

    nvme_bullets = [
        ("Form Factor:", "Standard 2280 (22mm wide × 80mm long) naked circuit board stick."),
        ("Edge Connector:", "M-Key connector (5 pins, notch, 33 pins) slots directly into motherboard."),
        ("Direct Bus:", "Bypasses slow SATA controller; links directly to CPU via PCIe 4.0/5.0 x4 lanes."),
        ("Throughput:", "Up to 14x faster than SATA SSDs; ultra-low microsecond latency (<20 µs)."),
        ("Best Use Case:", "Primary operating system boot drive, high-end workstations, & gaming."),
    ]
    cy = CARD_Y + 98
    for lbl, txt in nvme_bullets:
        draw.ellipse([c3_x + 20, cy + 5, c3_x + 26, cy + 11], fill=c_nvme["accent"])
        draw.text((c3_x + 34, cy), lbl, fill=(241, 245, 249), font=fonts["body_bold"])
        l_len = draw.textlength(lbl + " ", font=fonts["body_bold"])
        draw.text((c3_x + 34 + l_len, cy), txt, fill=(203, 213, 225), font=fonts["body"])
        cy += 28

    final_img = Image.alpha_composite(canvas, overlay).convert("RGB")
    final_img.save(out_path, quality=95)
    print(f"Generated storage diagram to {out_path}")

if __name__ == "__main__":
    photo_src = r"C:\Users\mlingsch\.gemini\antigravity-ide\brain\867def5a-de8f-410a-b81b-24b42c7de709\storage_nvme_sata_hdd_comparison_1788874929995.jpg"
    out_path = "public/images/tech-plus/storage-form-factors-nvme-sata-hdd.jpg"
    generate_storage_diagram(photo_src, out_path)
