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
        "body": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14),
        "small": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13),
        "step_num": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20),
    }

def draw_wrapped_text(draw, x, y, text, font, fill, max_width, line_spacing=22):
    words = text.split(" ")
    lines = []
    curr_line = ""
    for w in words:
        test_line = curr_line + (" " if curr_line else "") + w
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w_px = bbox[2] - bbox[0]
        if w_px <= max_width:
            curr_line = test_line
        else:
            if curr_line:
                lines.append(curr_line)
            curr_line = w
    if curr_line:
        lines.append(curr_line)
    
    curr_y = y
    for line in lines:
        draw.text((x, curr_y), line, fill=fill, font=font)
        curr_y += line_spacing
    return curr_y

def generate_crypto_diagram(out_path):
    W, H = 2500, 1400
    img = Image.new("RGBA", (W, H), (10, 15, 29, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fonts = get_fonts()

    # Header
    draw.text((60, 32), "CRYPTOGRAPHY ARCHITECTURE: SYMMETRIC, ASYMMETRIC & HYBRID TLS", fill=(248, 250, 252), font=fonts["header"])
    draw.text((64, 82), "CompTIA Tech+ FC0-U71: Plaintext vs. Ciphertext, Shared Secrets (AES), Key Pairs (RSA/ECC), and HTTPS Handshakes", fill=(148, 163, 184), font=fonts["subhdr"])

    # -------------------------------------------------------------
    # TOP HALF: SYMMETRIC VS ASYMMETRIC (y: 130 to 760)
    # -------------------------------------------------------------
    top_y = 130
    top_h = 630
    panel_w = 1170
    gap = 40

    # ------------------ LEFT: SYMMETRIC CIPHERS ------------------
    p1_x = 60
    draw.rounded_rectangle([p1_x, top_y, p1_x + panel_w, top_y + top_h], radius=14, fill=(16, 24, 40, 255), outline=(52, 211, 153, 220), width=2)

    # Title Badge
    draw.rounded_rectangle([p1_x + 20, top_y + 16, p1_x + 20 + 410, top_y + 16 + 30], radius=6, fill=(16, 185, 129, 255))
    draw.text((p1_x + 35, top_y + 20), "SYMMETRIC ENCRYPTION (SHARED KEY)", fill=(10, 15, 29), font=fonts["section_title"])
    draw.text((p1_x + 450, top_y + 20), "One identical secret key locks and unlocks data", fill=(203, 213, 225), font=fonts["subhdr"])

    # Visual Flow Box (Symmetric Pipeline)
    flow1_y = top_y + 65
    flow1_h = 175
    draw.rounded_rectangle([p1_x + 20, flow1_y, p1_x + panel_w - 20, flow1_y + flow1_h], radius=10, fill=(11, 19, 36), outline=(52, 211, 153, 100), width=1)

    # Stages in Symmetric Flow:
    # A: Plaintext
    draw.rounded_rectangle([p1_x + 40, flow1_y + 25, p1_x + 300, flow1_y + 145], radius=8, fill=(15, 28, 48), outline=(148, 163, 184, 150), width=1)
    draw.text((p1_x + 55, flow1_y + 38), "PLAINTEXT", fill=(248, 250, 252), font=fonts["badge"])
    draw.text((p1_x + 55, flow1_y + 68), '"Confidential Payroll"', fill=(52, 211, 153), font=fonts["box_title"])
    draw.text((p1_x + 55, flow1_y + 102), "Readable original text", fill=(148, 163, 184), font=fonts["small"])

    # Arrow 1 -> Key Lock
    draw.line([p1_x + 315, flow1_y + 85, p1_x + 375, flow1_y + 85], fill=(52, 211, 153), width=3)
    draw.polygon([(p1_x + 375, flow1_y + 80), (p1_x + 390, flow1_y + 85), (p1_x + 375, flow1_y + 90)], fill=(52, 211, 153))

    # Shared Key Center Box
    draw.rounded_rectangle([p1_x + 405, flow1_y + 20, p1_x + 725, flow1_y + 150], radius=8, fill=(12, 36, 28), outline=(52, 211, 153, 200), width=2)
    draw.text((p1_x + 425, flow1_y + 30), "SHARED SECRET KEY", fill=(52, 211, 153), font=fonts["box_title"])
    draw.text((p1_x + 425, flow1_y + 60), "Key: `k9$J#mQ8*zR...`", fill=(241, 245, 249), font=fonts["body_bold"])
    draw.text((p1_x + 425, flow1_y + 90), "• Single key encrypts AND decrypts", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p1_x + 425, flow1_y + 115), "• Algorithm: AES-256 GCM", fill=(52, 211, 153), font=fonts["small"])

    # Arrow 2 -> Ciphertext
    draw.line([p1_x + 740, flow1_y + 85, p1_x + 800, flow1_y + 85], fill=(52, 211, 153), width=3)
    draw.polygon([(p1_x + 800, flow1_y + 80), (p1_x + 815, flow1_y + 85), (p1_x + 800, flow1_y + 90)], fill=(52, 211, 153))

    # B: Ciphertext
    draw.rounded_rectangle([p1_x + 830, flow1_y + 25, p1_x + 1130, flow1_y + 145], radius=8, fill=(15, 28, 48), outline=(251, 146, 60, 150), width=1)
    draw.text((p1_x + 845, flow1_y + 38), "CIPHERTEXT", fill=(251, 146, 60), font=fonts["badge"])
    draw.text((p1_x + 845, flow1_y + 68), "`%8x#9!kL$2@vP9...`", fill=(251, 146, 60), font=fonts["box_title"])
    draw.text((p1_x + 845, flow1_y + 102), "Unreadable scrambled noise", fill=(148, 163, 184), font=fonts["small"])

    # Feature List Grid for Symmetric
    s_feat_y = flow1_y + flow1_h + 20
    s_col_w = (panel_w - 60) // 2

    # Col 1: Characteristics
    draw.rounded_rectangle([p1_x + 20, s_feat_y, p1_x + 20 + s_col_w, top_y + top_h - 20], radius=8, fill=(11, 19, 36), outline=(52, 211, 153, 70), width=1)
    draw.text((p1_x + 36, s_feat_y + 14), "Performance & Key Architecture", fill=(52, 211, 153), font=fonts["box_title"])
    draw.text((p1_x + 36, s_feat_y + 44), "• Execution Speed: ULTRA-FAST (Hardware AES-NI)", fill=(241, 245, 249), font=fonts["body_bold"])
    draw.text((p1_x + 50, s_feat_y + 68), "Native microsecond acceleration built into all CPUs.", fill=(148, 163, 184), font=fonts["small"])
    draw.text((p1_x + 36, s_feat_y + 96), "• Best For: Bulk Data Encryption at Scale", fill=(241, 245, 249), font=fonts["body_bold"])
    draw.text((p1_x + 50, s_feat_y + 120), "Encrypting TBs of files, NVMe drives, and live video.", fill=(148, 163, 184), font=fonts["small"])
    draw.text((p1_x + 36, s_feat_y + 148), "• The Key Distribution Dilemma:", fill=(251, 146, 60), font=fonts["body_bold"])
    draw.text((p1_x + 50, s_feat_y + 172), "How do you securely share this secret key over", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p1_x + 50, s_feat_y + 194), "the public internet without eavesdroppers stealing it?", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p1_x + 50, s_feat_y + 224), "Solved by: Asymmetric cryptography during TLS handshake.", fill=(52, 211, 153), font=fonts["small"])
    draw.text((p1_x + 50, s_feat_y + 254), "• Key Size: 128-bit, 192-bit, or 256-bit (AES-256 standard).", fill=(148, 163, 184), font=fonts["small"])
    draw.text((p1_x + 50, s_feat_y + 284), "• Resource Impact: Low CPU utilization & power consumption.", fill=(148, 163, 184), font=fonts["small"])

    # Col 2: Algorithms & Standards
    draw.rounded_rectangle([p1_x + 40 + s_col_w, s_feat_y, p1_x + panel_w - 20, top_y + top_h - 20], radius=8, fill=(11, 19, 36), outline=(52, 211, 153, 70), width=1)
    draw.text((p1_x + 56 + s_col_w, s_feat_y + 14), "Approved vs. Broken Ciphers (CompTIA)", fill=(52, 211, 153), font=fonts["box_title"])

    # Approved box
    draw.rounded_rectangle([p1_x + 56 + s_col_w, s_feat_y + 44, p1_x + panel_w - 36, s_feat_y + 160], radius=6, fill=(15, 28, 48), outline=(52, 211, 153, 120), width=1)
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 54), "[ APPROVED STANDARDS ]", fill=(52, 211, 153), font=fonts["badge"])
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 80), "• AES (Advanced Encryption Standard): 128 / 256-bit", fill=(241, 245, 249), font=fonts["body_bold"])
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 106), "• ChaCha20: Modern high-speed cipher for mobile / VPNs", fill=(203, 213, 225), font=fonts["body"])
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 132), "• Use Case: BitLocker, FileVault, WPA3 Wi-Fi, HTTPS streams", fill=(148, 163, 184), font=fonts["small"])

    # Broken box
    draw.rounded_rectangle([p1_x + 56 + s_col_w, s_feat_y + 175, p1_x + panel_w - 36, top_y + top_h - 36], radius=6, fill=(38, 20, 20), outline=(239, 68, 68, 150), width=1)
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 185), "[ BROKEN / DEPRECATED — EXAM TRAPS ]", fill=(239, 68, 68), font=fonts["badge"])
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 212), "• DES (Data Encryption Standard): 56-bit key (cracked in hours)", fill=(254, 202, 202), font=fonts["body"])
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 238), "• 3DES (Triple DES): Deprecated legacy standard", fill=(254, 202, 202), font=fonts["body"])
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 264), "• RC4: Broken stream cipher; vulnerable to plaintext leaks", fill=(254, 202, 202), font=fonts["body"])
    draw.text((p1_x + 70 + s_col_w, s_feat_y + 292), "RULE: Never deploy DES or RC4 in modern enterprise networks!", fill=(239, 68, 68), font=fonts["small"])

    # ------------------ RIGHT: ASYMMETRIC CIPHERS ------------------
    p2_x = p1_x + panel_w + gap
    draw.rounded_rectangle([p2_x, top_y, p2_x + panel_w, top_y + top_h], radius=14, fill=(16, 24, 40, 255), outline=(192, 132, 252, 220), width=2)

    # Title Badge
    draw.rounded_rectangle([p2_x + 20, top_y + 16, p2_x + 20 + 460, top_y + 16 + 30], radius=6, fill=(168, 85, 247, 255))
    draw.text((p2_x + 35, top_y + 20), "ASYMMETRIC ENCRYPTION (PUBLIC / PRIVATE)", fill=(10, 15, 29), font=fonts["section_title"])
    draw.text((p2_x + 500, top_y + 20), "Mathematically linked pair: Public encrypts, Private decrypts", fill=(203, 213, 225), font=fonts["subhdr"])

    # Visual Flow Box (Asymmetric Mailbox Flow)
    draw.rounded_rectangle([p2_x + 20, flow1_y, p2_x + panel_w - 20, flow1_y + flow1_h], radius=10, fill=(11, 19, 36), outline=(192, 132, 252, 100), width=1)

    # Stage 1: Sender (Bob)
    draw.rounded_rectangle([p2_x + 40, flow1_y + 25, p2_x + 300, flow1_y + 145], radius=8, fill=(15, 28, 48), outline=(56, 189, 248, 150), width=1)
    draw.text((p2_x + 55, flow1_y + 38), "SENDER (BOB)", fill=(56, 189, 248), font=fonts["badge"])
    draw.text((p2_x + 55, flow1_y + 68), "Encrypts with:", fill=(241, 245, 249), font=fonts["body"])
    draw.text((p2_x + 55, flow1_y + 92), "ALICE'S PUBLIC KEY", fill=(56, 189, 248), font=fonts["box_title"])
    draw.text((p2_x + 55, flow1_y + 120), "Freely published to anyone", fill=(148, 163, 184), font=fonts["small"])

    # Arrow 1 -> Public Internet / Ciphertext
    draw.line([p2_x + 315, flow1_y + 85, p2_x + 375, flow1_y + 85], fill=(192, 132, 252), width=3)
    draw.polygon([(p2_x + 375, flow1_y + 80), (p2_x + 390, flow1_y + 85), (p2_x + 375, flow1_y + 90)], fill=(192, 132, 252))

    # Stage 2: Transit / Lock Box (The Public Mailbox Analogy)
    draw.rounded_rectangle([p2_x + 405, flow1_y + 20, p2_x + 725, flow1_y + 150], radius=8, fill=(34, 16, 44), outline=(192, 132, 252, 200), width=2)
    draw.text((p2_x + 425, flow1_y + 30), "THE ONE-WAY MAILBOX", fill=(192, 132, 252), font=fonts["box_title"])
    draw.text((p2_x + 425, flow1_y + 58), "• Anyone can drop letters in slot", fill=(241, 245, 249), font=fonts["body"])
    draw.text((p2_x + 425, flow1_y + 84), "• Public Key = Mailbox Drop Slot", fill=(56, 189, 248), font=fonts["small"])
    draw.text((p2_x + 425, flow1_y + 108), "• Even Bob CANNOT open it back up!", fill=(251, 146, 60), font=fonts["small"])
    draw.text((p2_x + 425, flow1_y + 128), "• Only keyholder opens rear door", fill=(148, 163, 184), font=fonts["small"])

    # Arrow 2 -> Recipient (Alice)
    draw.line([p2_x + 740, flow1_y + 85, p2_x + 800, flow1_y + 85], fill=(192, 132, 252), width=3)
    draw.polygon([(p2_x + 800, flow1_y + 80), (p2_x + 815, flow1_y + 85), (p2_x + 800, flow1_y + 90)], fill=(192, 132, 252))

    # Stage 3: Recipient (Alice)
    draw.rounded_rectangle([p2_x + 830, flow1_y + 25, p2_x + 1130, flow1_y + 145], radius=8, fill=(15, 28, 48), outline=(192, 132, 252, 150), width=1)
    draw.text((p2_x + 845, flow1_y + 38), "RECIPIENT (ALICE)", fill=(192, 132, 252), font=fonts["badge"])
    draw.text((p2_x + 845, flow1_y + 68), "Decrypts with:", fill=(241, 245, 249), font=fonts["body"])
    draw.text((p2_x + 845, flow1_y + 92), "ALICE'S PRIVATE KEY", fill=(192, 132, 252), font=fonts["box_title"])
    draw.text((p2_x + 845, flow1_y + 120), "Kept strictly secret in HSM / TPM", fill=(52, 211, 153), font=fonts["small"])

    # Feature List Grid for Asymmetric
    draw.rounded_rectangle([p2_x + 20, s_feat_y, p2_x + 20 + s_col_w, top_y + top_h - 20], radius=8, fill=(11, 19, 36), outline=(192, 132, 252, 70), width=1)
    draw.text((p2_x + 36, s_feat_y + 14), "Performance & Key Architecture", fill=(192, 132, 252), font=fonts["box_title"])
    draw.text((p2_x + 36, s_feat_y + 44), "• Execution Speed: COMPUTATIONALLY HEAVY", fill=(251, 146, 60), font=fonts["body_bold"])
    draw.text((p2_x + 50, s_feat_y + 68), "Requires intense prime factorization or elliptic curves.", fill=(148, 163, 184), font=fonts["small"])
    draw.text((p2_x + 36, s_feat_y + 96), "• Key Distribution Solved Forever:", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((p2_x + 50, s_feat_y + 120), "Public keys are published on public directories / DNS.", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p2_x + 50, s_feat_y + 142), "No secret key needs to be transmitted across the wire.", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p2_x + 36, s_feat_y + 170), "• Primary Use Cases:", fill=(241, 245, 249), font=fonts["body_bold"])
    draw.text((p2_x + 50, s_feat_y + 194), "1. TLS/SSL Handshakes (exchanging symmetric keys)", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p2_x + 50, s_feat_y + 216), "2. Digital Signatures (Non-repudiation & authenticity)", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p2_x + 50, s_feat_y + 238), "3. SSH Authentication (Authorized_keys file)", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p2_x + 50, s_feat_y + 264), "• Key Size: RSA (2048-4096 bits) vs ECC (256-384 bits)", fill=(148, 163, 184), font=fonts["small"])
    draw.text((p2_x + 50, s_feat_y + 290), "• Security: Private key must NEVER leave the host machine!", fill=(239, 68, 68), font=fonts["small"])

    # Col 2: Standards & PKI
    draw.rounded_rectangle([p2_x + 40 + s_col_w, s_feat_y, p2_x + panel_w - 20, top_y + top_h - 20], radius=8, fill=(11, 19, 36), outline=(192, 132, 252, 70), width=1)
    draw.text((p2_x + 56 + s_col_w, s_feat_y + 14), "Approved Algorithms & Key Roles", fill=(192, 132, 252), font=fonts["box_title"])

    draw.rounded_rectangle([p2_x + 56 + s_col_w, s_feat_y + 44, p2_x + panel_w - 36, s_feat_y + 160], radius=6, fill=(15, 28, 48), outline=(192, 132, 252, 120), width=1)
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 54), "[ APPROVED ALGORITHMS ]", fill=(192, 132, 252), font=fonts["badge"])
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 80), "• RSA (Rivest-Shamir-Adleman): Minimum 2048-bit", fill=(241, 245, 249), font=fonts["body_bold"])
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 106), "• ECC (Elliptic Curve Cryptography): 256/384-bit", fill=(52, 211, 153), font=fonts["body_bold"])
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 132), "• Diffie-Hellman (DH / ECDH): Ephemeral key exchange", fill=(203, 213, 225), font=fonts["small"])

    draw.rounded_rectangle([p2_x + 56 + s_col_w, s_feat_y + 175, p2_x + panel_w - 36, top_y + top_h - 36], radius=6, fill=(15, 28, 48), outline=(56, 189, 248, 120), width=1)
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 185), "[ ASYMMETRIC KEY RULES ]", fill=(56, 189, 248), font=fonts["badge"])
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 212), "• Confidentiality: Encrypt with RECIPIENT'S PUBLIC KEY", fill=(56, 189, 248), font=fonts["body_bold"])
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 238), "  Only the recipient's private key can decrypt it.", fill=(203, 213, 225), font=fonts["small"])
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 264), "• Digital Signature: Sign with SENDER'S PRIVATE KEY", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((p2_x + 70 + s_col_w, s_feat_y + 290), "  Anyone with the public key verifies identity.", fill=(203, 213, 225), font=fonts["small"])

    # -------------------------------------------------------------
    # BOTTOM HALF: HYBRID TLS 1.3 ARCHITECTURE (y: 790 to 1340)
    # -------------------------------------------------------------
    bot_y = 790
    bot_h = 560
    draw.rounded_rectangle([60, bot_y, 2440, bot_y + bot_h], radius=14, fill=(16, 24, 40, 255), outline=(251, 146, 60, 220), width=2)

    # Title Badge
    draw.rounded_rectangle([80, bot_y + 16, 80 + 520, bot_y + 16 + 30], radius=6, fill=(249, 115, 22, 255))
    draw.text((95, bot_y + 20), "HYBRID ENCRYPTION: HOW TLS 1.3 POWERS HTTPS", fill=(10, 15, 29), font=fonts["section_title"])
    draw.text((620, bot_y + 20), "Combining the Key-Distribution Power of Asymmetric RSA with the Blazing Speed of Symmetric AES", fill=(203, 213, 225), font=fonts["subhdr"])

    # 4 Sequential Steps across the bottom width
    step_w = 560
    step_gap = 26
    step_h = 440
    step_y = bot_y + 65

    steps_data = [
        {
            "num": "STEP 1",
            "title": "Client Hello & Certificate",
            "badge_color": (56, 189, 248),
            "accent_color": (56, 189, 248),
            "points": [
                "• Action: Web browser initiates HTTPS request to bank website.",
                "• Certificate Sent: Web server responds with its X.509 Digital Certificate.",
                "• Public Key Included: Contains the bank server's Asymmetric Public Key.",
                "• CA Verification: Browser verifies certificate was signed by a trusted Root CA.",
                "• Defense: Prevents Man-in-the-Middle (MITM) spoofing.",
            ],
            "footer": "Method: Asymmetric Identity Proof"
        },
        {
            "num": "STEP 2",
            "title": "Generate Session Key",
            "badge_color": (52, 211, 153),
            "accent_color": (52, 211, 153),
            "points": [
                "• Action: Browser generates a fresh, pseudorandom 256-bit Symmetric Session Key in RAM.",
                "• Ephemeral Life: Session key exists exclusively for this single active browsing session.",
                "• Forward Secrecy: Modern TLS 1.3 ephemeral keys ensure past traffic cannot be cracked.",
                "• Status: Only the client has this key right now.",
            ],
            "footer": "Method: High-Entropy PRNG"
        },
        {
            "num": "STEP 3",
            "title": "Asymmetric Key Lock & Sync",
            "badge_color": (168, 85, 247),
            "accent_color": (168, 85, 247),
            "points": [
                "• Encrypt Key: Browser encrypts the Symmetric Session Key using the Server's Public Key.",
                "• Transmit: Ciphertext is sent over the public, untrusted internet.",
                "• Eavesdropper Safe: Hackers cannot decrypt without the private key.",
                "• Server Unlock: Server decrypts packet using its confidential Private Key.",
                "• Result: Both client and server now share the key!",
            ],
            "footer": "Method: Asymmetric Key Exchange"
        },
        {
            "num": "STEP 4",
            "title": "High-Speed Bulk AES Stream",
            "badge_color": (251, 146, 60),
            "accent_color": (251, 146, 60),
            "points": [
                "• Handshake Complete: Asymmetric crypto is turned OFF to save CPU power.",
                "• Symmetric Bulk Stream: All HTML, JSON, streaming video, and bank records use AES-256.",
                "• Speed: Zero lag or buffering; billions of packets per second processed effortlessly.",
                "• Summary: Asymmetric starts the call; Symmetric handles the conversation!",
            ],
            "footer": "Method: Symmetric AES-256 Bulk"
        },
    ]

    for i, s in enumerate(steps_data):
        sx = 80 + i * (step_w + step_gap)
        draw.rounded_rectangle([sx, step_y, sx + step_w, step_y + step_h], radius=10, fill=(11, 19, 36), outline=(*s["accent_color"], 180), width=2)
        
        # Step Number Badge
        draw.rounded_rectangle([sx + 16, step_y + 16, sx + 16 + 95, step_y + 16 + 30], radius=6, fill=s["badge_color"])
        draw.text((sx + 26, step_y + 19), s["num"], fill=(10, 15, 29), font=fonts["step_num"])

        # Title
        draw.text((sx + 125, step_y + 20), s["title"], fill=(248, 250, 252), font=fonts["box_title"])

        # Points (wrapped within card width)
        curr_py = step_y + 65
        for pt in s["points"]:
            curr_py = draw_wrapped_text(draw, sx + 16, curr_py, pt, fonts["body"], (203, 213, 225), max_width=step_w - 32, line_spacing=22)
            curr_py += 8

        # Footer Box
        draw.rounded_rectangle([sx + 16, step_y + step_h - 44, sx + step_w - 16, step_y + step_h - 14], radius=6, fill=(15, 28, 48), outline=(*s["accent_color"], 80), width=1)
        draw.text((sx + 26, step_y + step_h - 38), s["footer"], fill=s["accent_color"], font=fonts["badge"])

        # Draw arrow between cards if not last
        if i < 3:
            arrow_x = sx + step_w + 3
            arrow_y = step_y + step_h // 2
            draw.polygon([(arrow_x, arrow_y - 12), (arrow_x + 18, arrow_y), (arrow_x, arrow_y + 12)], fill=(148, 163, 184))

    # Combine
    final = Image.alpha_composite(img, overlay).convert("RGB")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final.save(out_path, quality=95)
    print(f"Generated crypto diagram: {out_path} ({W}x{H})")

if __name__ == "__main__":
    generate_crypto_diagram("public/images/tech-plus/cryptography-symmetric-vs-asymmetric.jpg")
