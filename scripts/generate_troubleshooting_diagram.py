import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    return {
        "header": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 42),
        "subhdr": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22),
        "card_num": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 28),
        "card_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 24),
        "badge": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15),
        "body_bold": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18),
        "body": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18),
        "note_bold": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16),
        "note": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16),
        "tip": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20),
    }

def draw_step_card(draw, fonts, x, y, w, h, step_num, title, badge_text, items, col):
    # Card background
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=col["bg"], outline=col["border"], width=2)

    # Number pill
    pill_w = 52
    pill_h = 48
    draw.rounded_rectangle([x + 20, y + 20, x + 20 + pill_w, y + 20 + pill_h], radius=10, fill=col["accent"])
    draw.text((x + 20 + 17, y + 20 + 5), str(step_num), fill=(10, 15, 29), font=fonts["card_num"])

    # Card Title
    draw.text((x + 86, y + 18), title, fill=(248, 250, 252), font=fonts["card_title"])

    # Badge
    badge_w = draw.textlength(badge_text, font=fonts["badge"])
    draw.rounded_rectangle([x + 86, y + 52, x + 86 + badge_w + 16, y + 52 + 24], radius=6, fill=(255, 255, 255, 18), outline=col["border"], width=1)
    draw.text((x + 94, y + 54), badge_text, fill=col["accent"], font=fonts["badge"])

    # Divider line
    draw.line([(x + 20, y + 90), (x + w - 20, y + 90)], fill=(255, 255, 255, 35), width=1)

    # Bullets
    curr_y = y + 108
    for prefix, text, is_alert in items:
        bullet_col = col["accent"] if not is_alert else (248, 113, 113)
        draw.ellipse([x + 24, curr_y + 6, x + 32, curr_y + 14], fill=bullet_col)
        draw.text((x + 42, curr_y), prefix, fill=(241, 245, 249), font=fonts["body_bold"])
        p_len = draw.textlength(prefix + " ", font=fonts["body_bold"])
        draw.text((x + 42 + p_len, curr_y), text, fill=(203, 213, 225), font=fonts["body"])
        curr_y += 38

def generate_troubleshooting_diagram(out_path):
    W, H = 2400, 1350
    img = Image.new("RGBA", (W, H), (10, 15, 29, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fonts = get_fonts()

    # Header
    draw.text((60, 45), "COMPTIA 6-STEP TROUBLESHOOTING METHODOLOGY", fill=(248, 250, 252), font=fonts["header"])
    draw.text((64, 102), "The industry-standard systematic diagnostic framework for PC technicians & cybersecurity professionals", fill=(148, 163, 184), font=fonts["subhdr"])

    # Colors
    c_rose = {"bg": (38, 14, 22, 250), "border": (244, 63, 94, 255), "accent": (244, 63, 94, 255), "glow": (244, 63, 94, 90)}
    c_amber = {"bg": (36, 26, 12, 250), "border": (251, 191, 36, 255), "accent": (251, 191, 36, 255), "glow": (251, 191, 36, 90)}
    c_sky = {"bg": (14, 30, 52, 250), "border": (56, 189, 248, 255), "accent": (56, 189, 248, 255), "glow": (56, 189, 248, 90)}
    c_indigo = {"bg": (22, 25, 58, 250), "border": (129, 140, 248, 255), "accent": (129, 140, 248, 255), "glow": (129, 140, 248, 90)}
    c_green = {"bg": (12, 38, 26, 250), "border": (52, 211, 153, 255), "accent": (52, 211, 153, 255), "glow": (52, 211, 153, 90)}
    c_purple = {"bg": (34, 18, 50, 250), "border": (192, 132, 252, 255), "accent": (192, 132, 252, 255), "glow": (192, 132, 252, 90)}

    # Grid parameters
    CARD_W = 715
    CARD_H = 370
    COL1_X = 60
    COL2_X = 842
    COL3_X = 1625
    ROW1_Y = 220
    ROW2_Y = 700

    # Draw Connecting Arrows (Row 1: 1 -> 2 -> 3)
    # Arrow 1 -> 2
    draw.line([(COL1_X + CARD_W + 10, ROW1_Y + CARD_H//2), (COL2_X - 18, ROW1_Y + CARD_H//2)], fill=(148, 163, 184, 200), width=5)
    draw.polygon([(COL2_X - 10, ROW1_Y + CARD_H//2), (COL2_X - 28, ROW1_Y + CARD_H//2 - 12), (COL2_X - 28, ROW1_Y + CARD_H//2 + 12)], fill=(148, 163, 184, 255))

    # Arrow 2 -> 3
    draw.line([(COL2_X + CARD_W + 10, ROW1_Y + CARD_H//2), (COL3_X - 18, ROW1_Y + CARD_H//2)], fill=(148, 163, 184, 200), width=5)
    draw.polygon([(COL3_X - 10, ROW1_Y + CARD_H//2), (COL3_X - 28, ROW1_Y + CARD_H//2 - 12), (COL3_X - 28, ROW1_Y + CARD_H//2 + 12)], fill=(148, 163, 184, 255))

    # Arrow 3 -> 4 (Downwards from col 3)
    draw.line([(COL3_X + CARD_W//2, ROW1_Y + CARD_H + 10), (COL3_X + CARD_W//2, ROW2_Y - 18)], fill=(148, 163, 184, 200), width=5)
    draw.polygon([(COL3_X + CARD_W//2, ROW2_Y - 10), (COL3_X + CARD_W//2 - 12, ROW2_Y - 28), (COL3_X + CARD_W//2 + 12, ROW2_Y - 28)], fill=(148, 163, 184, 255))

    # Arrow 4 -> 5 (Leftwards from col 3 to col 2)
    draw.line([(COL3_X - 18, ROW2_Y + CARD_H//2), (COL2_X + CARD_W + 10, ROW2_Y + CARD_H//2)], fill=(148, 163, 184, 200), width=5)
    draw.polygon([(COL2_X + CARD_W + 10, ROW2_Y + CARD_H//2), (COL2_X + CARD_W + 28, ROW2_Y + CARD_H//2 - 12), (COL2_X + CARD_W + 28, ROW2_Y + CARD_H//2 + 12)], fill=(148, 163, 184, 255))

    # Arrow 5 -> 6 (Leftwards from col 2 to col 1)
    draw.line([(COL2_X - 18, ROW2_Y + CARD_H//2), (COL1_X + CARD_W + 10, ROW2_Y + CARD_H//2)], fill=(148, 163, 184, 200), width=5)
    draw.polygon([(COL1_X + CARD_W + 10, ROW2_Y + CARD_H//2), (COL1_X + CARD_W + 28, ROW2_Y + CARD_H//2 - 12), (COL1_X + CARD_W + 28, ROW2_Y + CARD_H//2 + 12)], fill=(148, 163, 184, 255))

    # Prominent Feedback Loop Pill (Step 3 -> Step 2)
    loop_y = 158
    p3_x = COL3_X + CARD_W//2
    p2_x = COL2_X + CARD_W//2
    draw.line([(p3_x, ROW1_Y - 5), (p3_x, loop_y + 16)], fill=(239, 68, 68, 220), width=4)
    draw.line([(p3_x, loop_y + 16), (p2_x, loop_y + 16)], fill=(239, 68, 68, 220), width=4)
    draw.line([(p2_x, loop_y + 16), (p2_x, ROW1_Y - 14)], fill=(239, 68, 68, 220), width=4)
    draw.polygon([(p2_x, ROW1_Y - 5), (p2_x - 10, ROW1_Y - 20), (p2_x + 10, ROW1_Y - 20)], fill=(239, 68, 68, 255))

    # Badge on the feedback line
    tag_w = 560
    tag_x = (p2_x + p3_x) // 2 - tag_w // 2
    draw.rounded_rectangle([tag_x, loop_y - 4, tag_x + tag_w, loop_y + 36], radius=8, fill=(40, 15, 20), outline=(239, 68, 68), width=2)
    draw.text((tag_x + 20, loop_y + 3), "THEORY DISPROVED?  ->  Loop back to Step 2 to form new theory", fill=(248, 113, 113), font=fonts["note_bold"])

    # Step 1 Card
    s1_items = [
        ("Information Gathering:", "Interview user, inspect error logs & device.", False),
        ("Replication:", "Observe symptoms directly & duplicate fault.", False),
        ("Recent Changes:", "Determine what software/hardware changed.", False),
        ("Layered Scope:", "Approach multiple symptoms systematically.", False),
        ("Pre-Flight Backup:", "Back up user data before invasive triage.", False),
    ]
    draw_step_card(draw, fonts, COL1_X, ROW1_Y, CARD_W, CARD_H, 1, "Identify the Problem", "PHASE 1 · DISCOVERY", s1_items, c_rose)

    # Step 2 Card
    s2_items = [
        ("Question the Obvious:", "Cables secure, power on, caps lock, Wi-Fi switch?", False),
        ("Consider Causes:", "Internal vs. external, software vs. hardware.", False),
        ("Divide & Conquer:", "Isolate component or network layer in turn.", False),
        ("Knowledge Base:", "Research vendor documentation & internal KB.", False),
        ("Prioritize:", "Rank hypotheses from most obvious to complex.", False),
    ]
    draw_step_card(draw, fonts, COL2_X, ROW1_Y, CARD_W, CARD_H, 2, "Establish Theory of Cause", "PHASE 2 · HYPOTHESIS", s2_items, c_amber)

    # Step 3 Card
    s3_items = [
        ("Controlled Testing:", "Test isolated variable in safe environment.", False),
        ("Confirmed Cause:", "Proceed immediately to Step 4 action plan.", False),
        ("Disproved Cause:", "Formulate new theory or escalate to tier 2/3.", True),
        ("Escalation Gate:", "If beyond skill scope or permissions, escalate.", True),
        ("Safety Check:", "Ensure test does not damage customer equipment.", False),
    ]
    draw_step_card(draw, fonts, COL3_X, ROW1_Y, CARD_W, CARD_H, 3, "Test Theory to Determine Cause", "PHASE 3 · VERIFICATION", s3_items, c_sky)

    # Step 4 Card
    s4_items = [
        ("Action Plan:", "Draft specific chronological procedure to resolve.", False),
        ("Impact Assessment:", "Identify potential side-effects on production.", False),
        ("Change Management:", "Follow company approval policies if needed.", False),
        ("Implementation:", "Execute fix with rollback plan ready.", False),
        ("Safety Protocols:", "Observe ESD protection and proper tool handling.", False),
    ]
    draw_step_card(draw, fonts, COL3_X, ROW2_Y, CARD_W, CARD_H, 4, "Plan & Implement Solution", "PHASE 4 · REMEDIATION", s4_items, c_indigo)

    # Step 5 Card
    s5_items = [
        ("System Verification:", "Confirm full functionality across entire device.", False),
        ("User Acceptance:", "Have user test and verify problem is gone.", False),
        ("Preventive Measures:", "Install OS updates, UPS battery, or surge strip.", False),
        ("User Coaching:", "Brief user gently on best practices if PEBKAC.", False),
        ("Monitoring:", "Check performance metrics post-deployment.", False),
    ]
    draw_step_card(draw, fonts, COL2_X, ROW2_Y, CARD_W, CARD_H, 5, "Verify Full Functionality", "PHASE 5 · ASSURANCE", s5_items, c_green)

    # Step 6 Card
    s6_items = [
        ("Ticket Documentation:", "Record exact symptoms, root cause, and fix.", False),
        ("Parts & Time Logged:", "Document replaced components and labor time.", False),
        ("Knowledge Base:", "Add unique issues to team knowledge base.", False),
        ("Customer Hand-off:", "Deliver clear work summary to client.", False),
        ("Closure Sign-off:", "Close ticket with verified resolution code.", False),
    ]
    draw_step_card(draw, fonts, COL1_X, ROW2_Y, CARD_W, CARD_H, 6, "Document Findings & Actions", "PHASE 6 · KNOWLEDGE", s6_items, c_purple)

    # Footer note bar
    draw.rounded_rectangle([60, 1140, 2340, 1220], radius=12, fill=(18, 24, 38), outline=(56, 189, 248, 100), width=2)
    draw.text((90, 1167), "EXAM RULE (CompTIA Tech+): Always verify full system functionality (Step 5) BEFORE documenting (Step 6). Never close a ticket without documentation.", fill=(56, 189, 248), font=fonts["tip"])

    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    final_img.save(out_path, quality=95)
    print(f"Generated refined troubleshooting diagram to {out_path}")

if __name__ == "__main__":
    generate_troubleshooting_diagram("public/images/tech-plus/comptia-6-step-troubleshooting.jpg")
