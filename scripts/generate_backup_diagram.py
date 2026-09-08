import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    return {
        "header": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36),
        "subhdr": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20),
        "section_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20),
        "badge": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15),
        "box_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18),
        "body_bold": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15),
        "body": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15),
        "small": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13),
        "metric_val": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26),
    }

def generate_backup_diagram(out_path):
    W, H = 2500, 1400
    img = Image.new("RGBA", (W, H), (10, 15, 29, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fonts = get_fonts()

    # Header
    draw.text((60, 32), "DATA BACKUP ARCHITECTURE & DISASTER RECOVERY METRICS", fill=(248, 250, 252), font=fonts["header"])
    draw.text((64, 82), "CompTIA Tech+ FC0-U71: The 3-2-1 Backup Rule, Full vs. Incremental vs. Differential, and RTO / RPO Objectives", fill=(148, 163, 184), font=fonts["subhdr"])

    # -------------------------------------------------------------
    # TOP HALF: THE 3-2-1 BACKUP RULE (y: 130 to 640)
    # -------------------------------------------------------------
    top_y = 130
    top_h = 510
    draw.rounded_rectangle([60, top_y, 2440, top_y + top_h], radius=14, fill=(16, 24, 40, 255), outline=(56, 189, 248, 220), width=2)

    # Top Section Title Badge
    draw.rounded_rectangle([80, top_y + 16, 80 + 340, top_y + 16 + 30], radius=6, fill=(56, 189, 248, 255))
    draw.text((95, top_y + 20), "THE 3-2-1 BACKUP RULE", fill=(10, 15, 29), font=fonts["section_title"])
    draw.text((440, top_y + 20), "The industry standard framework for business continuity and disaster survival", fill=(203, 213, 225), font=fonts["subhdr"])

    col_w = 760
    col_gap = 30
    col_y = top_y + 65
    col_h = 420

    # Column 1: 3 COPIES OF DATA
    c1_x = 80
    draw.rounded_rectangle([c1_x, col_y, c1_x + col_w, col_y + col_h], radius=10, fill=(11, 19, 36, 255), outline=(52, 211, 153, 180), width=2)
    # Col 1 Header
    draw.rounded_rectangle([c1_x + 16, col_y + 16, c1_x + 16 + 180, col_y + 16 + 28], radius=6, fill=(16, 185, 129, 255))
    draw.text((c1_x + 26, col_y + 20), "3 TOTAL COPIES", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((c1_x + 210, col_y + 20), "Never rely on a single point of failure", fill=(148, 163, 184), font=fonts["body"])

    # Box 1A: Copy 1 (Primary)
    b1a_y = col_y + 60
    draw.rounded_rectangle([c1_x + 16, b1a_y, c1_x + col_w - 16, b1a_y + 90], radius=8, fill=(15, 28, 48), outline=(52, 211, 153, 80), width=1)
    draw.text((c1_x + 30, b1a_y + 12), "Copy 1: Primary Production Data (Live)", fill=(52, 211, 153), font=fonts["box_title"])
    draw.text((c1_x + 30, b1a_y + 38), "• Location: Live Server / Workstation SSD (e.g., C:\\Database)", fill=(241, 245, 249), font=fonts["body"])
    draw.text((c1_x + 30, b1a_y + 62), "• Purpose: Active business transactions, customer files, and daily operations", fill=(148, 163, 184), font=fonts["small"])

    # Box 1B: Copy 2 (Secondary Local)
    b1b_y = b1a_y + 105
    draw.rounded_rectangle([c1_x + 16, b1b_y, c1_x + col_w - 16, b1b_y + 90], radius=8, fill=(15, 28, 48), outline=(52, 211, 153, 80), width=1)
    draw.text((c1_x + 30, b1b_y + 12), "Copy 2: Local On-Premises Backup", fill=(52, 211, 153), font=fonts["box_title"])
    draw.text((c1_x + 30, b1b_y + 38), "• Location: Network Attached Storage (NAS) / Local Backup Server", fill=(241, 245, 249), font=fonts["body"])
    draw.text((c1_x + 30, b1b_y + 62), "• Purpose: Rapid local recovery over LAN without saturating WAN bandwidth", fill=(148, 163, 184), font=fonts["small"])

    # Box 1C: Copy 3 (Tertiary Cloud/Vault)
    b1c_y = b1b_y + 105
    draw.rounded_rectangle([c1_x + 16, b1c_y, c1_x + col_w - 16, b1c_y + 90], radius=8, fill=(15, 28, 48), outline=(52, 211, 153, 80), width=1)
    draw.text((c1_x + 30, b1c_y + 12), "Copy 3: Off-Site Cloud / Tape Vault", fill=(52, 211, 153), font=fonts["box_title"])
    draw.text((c1_x + 30, b1c_y + 38), "• Location: Secure Cloud Datacenter (AWS S3, Azure) or Offline Vault", fill=(241, 245, 249), font=fonts["body"])
    draw.text((c1_x + 30, b1c_y + 62), "• Purpose: Ultimate insurance if the physical facility suffers catastrophic loss", fill=(148, 163, 184), font=fonts["small"])

    # Column 2: 2 MEDIA TYPES
    c2_x = c1_x + col_w + col_gap
    draw.rounded_rectangle([c2_x, col_y, c2_x + col_w, col_y + col_h], radius=10, fill=(11, 19, 36, 255), outline=(56, 189, 248, 180), width=2)
    # Col 2 Header
    draw.rounded_rectangle([c2_x + 16, col_y + 16, c2_x + 16 + 210, col_y + 16 + 28], radius=6, fill=(14, 165, 233, 255))
    draw.text((c2_x + 26, col_y + 20), "2 DIFFERENT MEDIA", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((c2_x + 240, col_y + 20), "Mitigate common-cause hardware defects", fill=(148, 163, 184), font=fonts["body"])

    # Box 2A: Media Type 1 (Solid-State / Flash)
    b2a_y = col_y + 60
    draw.rounded_rectangle([c2_x + 16, b2a_y, c2_x + col_w - 16, b2a_y + 130], radius=8, fill=(15, 28, 48), outline=(56, 189, 248, 80), width=1)
    draw.text((c2_x + 30, b2a_y + 14), "Media Type A: Solid-State Flash (NVMe / SATA SSD)", fill=(56, 189, 248), font=fonts["box_title"])
    draw.text((c2_x + 30, b2a_y + 42), "• Technology: NAND flash memory chips with microsecond latencies", fill=(241, 245, 249), font=fonts["body"])
    draw.text((c2_x + 30, b2a_y + 68), "• Strengths: Unmatched read/write throughput for live database execution", fill=(203, 213, 225), font=fonts["body"])
    draw.text((c2_x + 30, b2a_y + 94), "• Risk: Controller bricking or voltage surges can kill entire drive at once", fill=(251, 146, 60), font=fonts["small"])

    # Box 2B: Media Type 2 (Magnetic Platter / Object Store)
    b2b_y = b2a_y + 145
    draw.rounded_rectangle([c2_x + 16, b2b_y, c2_x + col_w - 16, b2b_y + 165], radius=8, fill=(15, 28, 48), outline=(56, 189, 248, 80), width=1)
    draw.text((c2_x + 30, b2b_y + 14), "Media Type B: Magnetic Disk / LTO Tape / Cloud Object", fill=(56, 189, 248), font=fonts["box_title"])
    draw.text((c2_x + 30, b2b_y + 42), "• Technology: Multi-terabyte spinning HDD RAID array or LTO tape cartridges", fill=(241, 245, 249), font=fonts["body"])
    draw.text((c2_x + 30, b2b_y + 68), "• Strengths: High density, low cost-per-gigabyte, excellent archival life", fill=(203, 213, 225), font=fonts["body"])
    draw.text((c2_x + 30, b2b_y + 94), "• Independence: If flash firmware corrupts, magnetic copies remain readable", fill=(203, 213, 225), font=fonts["body"])
    draw.text((c2_x + 30, b2b_y + 122), "• Tech Tip: Never store backups exclusively on the exact same drive model!", fill=(148, 163, 184), font=fonts["small"])

    # Column 3: 1 OFF-SITE & IMMUTABLE
    c3_x = c2_x + col_w + col_gap
    draw.rounded_rectangle([c3_x, col_y, c3_x + col_w, col_y + col_h], radius=10, fill=(11, 19, 36, 255), outline=(251, 146, 60, 180), width=2)
    # Col 3 Header
    draw.rounded_rectangle([c3_x + 16, col_y + 16, c3_x + 16 + 200, col_y + 16 + 28], radius=6, fill=(249, 115, 22, 255))
    draw.text((c3_x + 26, col_y + 20), "1 OFF-SITE COPY", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((c3_x + 230, col_y + 20), "Survive physical and cyber catastrophe", fill=(148, 163, 184), font=fonts["body"])

    # Box 3A: Off-Site Isolation
    b3a_y = col_y + 60
    draw.rounded_rectangle([c3_x + 16, b3a_y, c3_x + col_w - 16, b3a_y + 130], radius=8, fill=(15, 28, 48), outline=(251, 146, 60, 80), width=1)
    draw.text((c3_x + 30, b3a_y + 14), "Geographic Separation (500+ Miles Away)", fill=(251, 146, 60), font=fonts["box_title"])
    draw.text((c3_x + 30, b3a_y + 42), "• Threat: Building fire, flood, hurricane, structural collapse, burglary", fill=(241, 245, 249), font=fonts["body"])
    draw.text((c3_x + 30, b3a_y + 68), "• Defense: If the primary office is destroyed, data survives off-site intact", fill=(203, 213, 225), font=fonts["body"])
    draw.text((c3_x + 30, b3a_y + 94), "• Architecture: Secure TLS sync to remote regional datacenter / cold storage", fill=(148, 163, 184), font=fonts["small"])

    # Box 3B: Immutable / Ransomware Defense
    b3b_y = b3a_y + 145
    draw.rounded_rectangle([c3_x + 16, b3b_y, c3_x + col_w - 16, b3b_y + 165], radius=8, fill=(15, 28, 48), outline=(251, 146, 60, 80), width=1)
    draw.text((c3_x + 30, b3b_y + 14), "Immutable WORM Policy (Ransomware Armor)", fill=(251, 146, 60), font=fonts["box_title"])
    draw.text((c3_x + 30, b3b_y + 42), "• WORM = Write Once, Read Many: Data cannot be altered once written", fill=(241, 245, 249), font=fonts["body"])
    draw.text((c3_x + 30, b3b_y + 68), "• Cryptographic Lock: Locked for 30-90 days against edits or deletion", fill=(203, 213, 225), font=fonts["body"])
    draw.text((c3_x + 30, b3b_y + 94), "• Zero Admin Overrides: Even if Domain Admin is hacked, backups are safe", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((c3_x + 30, b3b_y + 122), "• Air-gap principle: Backups cannot be encrypted by local malware", fill=(148, 163, 184), font=fonts["small"])

    # -------------------------------------------------------------
    # BOTTOM HALF LEFT: BACKUP TYPES COMPARISON (y: 670 to 1340, x: 60 to 1210)
    # -------------------------------------------------------------
    bot_y = 670
    bot_h = 680
    b_left_w = 1150
    draw.rounded_rectangle([60, bot_y, 60 + b_left_w, bot_y + bot_h], radius=14, fill=(16, 24, 40, 255), outline=(192, 132, 252, 220), width=2)

    # Title Badge
    draw.rounded_rectangle([80, bot_y + 16, 80 + 350, bot_y + 16 + 30], radius=6, fill=(168, 85, 247, 255))
    draw.text((95, bot_y + 20), "BACKUP TYPES & RESTORE PATHS", fill=(10, 15, 29), font=fonts["section_title"])
    draw.text((450, bot_y + 20), "Speed vs. Storage vs. Recovery Complexity", fill=(203, 213, 225), font=fonts["subhdr"])

    card_w = b_left_w - 40
    card_h = 180
    c_start_y = bot_y + 65

    # Card 1: FULL BACKUP
    card1_y = c_start_y
    draw.rounded_rectangle([80, card1_y, 80 + card_w, card1_y + card_h], radius=10, fill=(11, 19, 36), outline=(168, 85, 247, 100), width=1)
    draw.rounded_rectangle([96, card1_y + 14, 96 + 130, card1_y + 14 + 24], radius=5, fill=(168, 85, 247))
    draw.text((106, card1_y + 17), "FULL BACKUP", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((240, card1_y + 16), "Copies 100% of all files regardless of changes", fill=(241, 245, 249), font=fonts["box_title"])
    draw.text((96, card1_y + 48), "• Backup Speed: SLOWEST (transfers entire system dataset every time)", fill=(203, 213, 225), font=fonts["body"])
    draw.text((96, card1_y + 76), "• Storage Consumed: HIGHEST (requires massive disk/tape capacity)", fill=(203, 213, 225), font=fonts["body"])
    draw.text((96, card1_y + 104), "• Restoration Process: FASTEST & SIMPLEST — Requires exactly 1 backup set", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((96, card1_y + 134), "• Archive Bit: Clears the archive bit (flags all files as currently backed up)", fill=(148, 163, 184), font=fonts["small"])

    # Card 2: INCREMENTAL BACKUP
    card2_y = card1_y + card_h + 16
    draw.rounded_rectangle([80, card2_y, 80 + card_w, card2_y + card_h], radius=10, fill=(11, 19, 36), outline=(56, 189, 248, 100), width=1)
    draw.rounded_rectangle([96, card2_y + 14, 96 + 210, card2_y + 14 + 24], radius=5, fill=(56, 189, 248))
    draw.text((106, card2_y + 17), "INCREMENTAL BACKUP", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((320, card2_y + 16), "Copies ONLY files modified since the LAST backup (Full or Inc)", fill=(241, 245, 249), font=fonts["box_title"])
    draw.text((96, card2_y + 48), "• Backup Speed: FASTEST (only backs up small daily delta changes)", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((96, card2_y + 76), "• Storage Consumed: LOWEST (minimal daily footprint on storage pool)", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((96, card2_y + 104), "• Restoration Process: SLOWEST — Requires Last Full + ALL Incrementals in order", fill=(251, 146, 60), font=fonts["body_bold"])
    draw.text((96, card2_y + 134), "• Risk: If Tuesday's tape is corrupted, Wednesday and Thursday cannot be recovered!", fill=(248, 113, 113), font=fonts["small"])

    # Card 3: DIFFERENTIAL BACKUP
    card3_y = card2_y + card_h + 16
    draw.rounded_rectangle([80, card3_y, 80 + card_w, card3_y + card_h], radius=10, fill=(11, 19, 36), outline=(251, 146, 60, 100), width=1)
    draw.rounded_rectangle([96, card3_y + 14, 96 + 220, card3_y + 14 + 24], radius=5, fill=(251, 146, 60))
    draw.text((106, card3_y + 17), "DIFFERENTIAL BACKUP", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((330, card3_y + 16), "Copies ALL files modified since the LAST FULL backup only", fill=(241, 245, 249), font=fonts["box_title"])
    draw.text((96, card3_y + 48), "• Backup Speed: MODERATE (grows larger every day until the next Full backup)", fill=(203, 213, 225), font=fonts["body"])
    draw.text((96, card3_y + 76), "• Storage Consumed: MODERATE (cumulative changes saved daily)", fill=(203, 213, 225), font=fonts["body"])
    draw.text((96, card3_y + 104), "• Restoration Process: FAST — Requires exactly 2 sets: Last Full + LATEST Differential", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((96, card3_y + 134), "• Archive Bit: Does NOT clear archive bits; continues tracking cumulative delta", fill=(148, 163, 184), font=fonts["small"])

    # -------------------------------------------------------------
    # BOTTOM HALF RIGHT: RTO VS RPO TIMELINE (y: 670 to 1340, x: 1250 to 2440)
    # -------------------------------------------------------------
    b_right_x = 1250
    b_right_w = 1190
    draw.rounded_rectangle([b_right_x, bot_y, b_right_x + b_right_w, bot_y + bot_h], radius=14, fill=(16, 24, 40, 255), outline=(244, 63, 94, 220), width=2)

    # Title Badge
    draw.rounded_rectangle([b_right_x + 20, bot_y + 16, b_right_x + 20 + 440, bot_y + 16 + 30], radius=6, fill=(244, 63, 94, 255))
    draw.text((b_right_x + 35, bot_y + 20), "RTO vs. RPO: DISASTER RECOVERY TIMELINE", fill=(10, 15, 29), font=fonts["section_title"])
    draw.text((b_right_x + 480, bot_y + 20), "Business Continuity Targets Measured in Time", fill=(203, 213, 225), font=fonts["subhdr"])

    # VISUAL TIMELINE BOX
    tl_box_y = bot_y + 65
    tl_box_h = 240
    tl_box_w = b_right_w - 40
    draw.rounded_rectangle([b_right_x + 20, tl_box_y, b_right_x + 20 + tl_box_w, tl_box_y + tl_box_h], radius=10, fill=(11, 19, 36), outline=(148, 163, 184, 80), width=1)

    # Timeline horizontal line
    line_y = tl_box_y + 120
    draw.line([b_right_x + 60, line_y, b_right_x + tl_box_w - 20, line_y], fill=(71, 85, 105), width=4)

    # Points on line:
    # 1. Last Valid Backup (x: b_right_x + 100)
    pt1_x = b_right_x + 140
    # 2. Disaster Incident (x: b_right_x + 580)
    pt2_x = b_right_x + 580
    # 3. System Restored (x: b_right_x + 1020)
    pt3_x = b_right_x + 1020

    # Shaded Region 1: RPO (Data Loss Window) between pt1 and pt2
    draw.rounded_rectangle([pt1_x, line_y - 35, pt2_x, line_y + 35], radius=6, fill=(239, 68, 68, 50), outline=(239, 68, 68, 180), width=2)
    # Shaded Region 2: RTO (Downtime Window) between pt2 and pt3
    draw.rounded_rectangle([pt2_x, line_y - 35, pt3_x, line_y + 35], radius=6, fill=(59, 130, 246, 50), outline=(59, 130, 246, 180), width=2)

    # Markers
    # Point 1 Marker
    draw.ellipse([pt1_x - 12, line_y - 12, pt1_x + 12, line_y + 12], fill=(52, 211, 153), outline=(241, 245, 249), width=2)
    draw.text((pt1_x - 70, line_y - 75), "LAST VALID BACKUP", fill=(52, 211, 153), font=fonts["badge"])
    draw.text((pt1_x - 60, line_y - 52), "(Point in time saved)", fill=(148, 163, 184), font=fonts["small"])

    # Point 2 Marker (Disaster)
    draw.ellipse([pt2_x - 14, line_y - 14, pt2_x + 14, line_y + 14], fill=(239, 68, 68), outline=(255, 255, 255), width=3)
    draw.text((pt2_x - 80, line_y - 85), "[ ! ] DISASTER OCCURS", fill=(239, 68, 68), font=fonts["box_title"])
    draw.text((pt2_x - 85, line_y - 60), "(Crash / Ransomware / Fire)", fill=(248, 113, 113), font=fonts["small"])

    # Point 3 Marker (Restored)
    draw.ellipse([pt3_x - 12, line_y - 12, pt3_x + 12, line_y + 12], fill=(56, 189, 248), outline=(241, 245, 249), width=2)
    draw.text((pt3_x - 70, line_y - 75), "SERVICES RESTORED", fill=(56, 189, 248), font=fonts["badge"])
    draw.text((pt3_x - 60, line_y - 52), "(Operations normal)", fill=(148, 163, 184), font=fonts["small"])

    # Inside Shaded Labels
    # RPO Label
    draw.text((pt1_x + 100, line_y - 14), "RPO: DATA LOSS WINDOW", fill=(254, 202, 202), font=fonts["body_bold"])
    draw.text((pt1_x + 50, line_y + 46), "Transactions created in this window are lost", fill=(252, 165, 165), font=fonts["small"])

    # RTO Label
    draw.text((pt2_x + 110, line_y - 14), "RTO: SYSTEM DOWNTIME", fill=(191, 219, 254), font=fonts["body_bold"])
    draw.text((pt2_x + 60, line_y + 46), "Time spent repairing, restoring, and booting", fill=(147, 197, 253), font=fonts["small"])

    # Metric Comparison Cards below Timeline
    met_y = tl_box_y + tl_box_h + 16
    met_w = (tl_box_w - 20) // 2
    met_h = 320

    # RPO Card
    draw.rounded_rectangle([b_right_x + 20, met_y, b_right_x + 20 + met_w, met_y + met_h], radius=10, fill=(11, 19, 36), outline=(239, 68, 68, 120), width=1)
    draw.text((b_right_x + 36, met_y + 16), "RPO: Recovery Point Objective", fill=(239, 68, 68), font=fonts["box_title"])
    draw.text((b_right_x + 36, met_y + 48), '"How much data can we afford to lose?"', fill=(254, 202, 202), font=fonts["subhdr"])
    draw.text((b_right_x + 36, met_y + 90), "• Measured in: Time (Minutes, Hours, or Days)", fill=(241, 245, 249), font=fonts["body"])
    draw.text((b_right_x + 36, met_y + 120), "• Dictates: BACKUP FREQUENCY", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((b_right_x + 36, met_y + 150), "• Real-World Rule:", fill=(203, 213, 225), font=fonts["body"])
    draw.text((b_right_x + 50, met_y + 175), "If RPO is 15 minutes, you MUST execute backups", fill=(203, 213, 225), font=fonts["body"])
    draw.text((b_right_x + 50, met_y + 200), "or continuous database replication every 15 min.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((b_right_x + 36, met_y + 240), "• Exam Trap: Backing up once a day violates any RPO under 24 hours!", fill=(251, 146, 60), font=fonts["small"])

    # RTO Card
    rto_x = b_right_x + 20 + met_w + 20
    draw.rounded_rectangle([rto_x, met_y, rto_x + met_w, met_y + met_h], radius=10, fill=(11, 19, 36), outline=(59, 130, 246, 120), width=1)
    draw.text((rto_x + 16, met_y + 16), "RTO: Recovery Time Objective", fill=(59, 130, 246), font=fonts["box_title"])
    draw.text((rto_x + 16, met_y + 48), '"How long can we afford to be down?"', fill=(191, 219, 254), font=fonts["subhdr"])
    draw.text((rto_x + 16, met_y + 90), "• Measured in: Time (Hours or Business Days)", fill=(241, 245, 249), font=fonts["body"])
    draw.text((rto_x + 16, met_y + 120), "• Dictates: RESTORATION SPEED & REDUNDANCY", fill=(56, 189, 248), font=fonts["body_bold"])
    draw.text((rto_x + 16, met_y + 150), "• Real-World Rule:", fill=(203, 213, 225), font=fonts["body"])
    draw.text((rto_x + 30, met_y + 175), "If RTO is 2 hours, restoring a 20TB database over", fill=(203, 213, 225), font=fonts["body"])
    draw.text((rto_x + 30, met_y + 200), "a slow 100Mbps cloud link will fail SLA guarantees.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((rto_x + 16, met_y + 240), "• Solution: Fast local NAS disk images or Hot Standby failover servers.", fill=(52, 211, 153), font=fonts["small"])

    # Combine
    final = Image.alpha_composite(img, overlay).convert("RGB")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final.save(out_path, quality=95)
    print(f"Generated backup diagram: {out_path} ({W}x{H})")

if __name__ == "__main__":
    generate_backup_diagram("public/images/tech-plus/backup-3-2-1-rule-rto-rpo.jpg")
