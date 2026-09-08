import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    return {
        "header": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38),
        "subhdr": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 21),
        "tier_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22),
        "badge": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14),
        "box_title": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18),
        "body_bold": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15),
        "body": ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15),
        "gate": ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17),
    }

def generate_os_architecture_diagram(out_path):
    W, H = 2500, 1400
    img = Image.new("RGBA", (W, H), (10, 15, 29, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    fonts = get_fonts()

    # Header
    draw.text((60, 35), "OPERATING SYSTEM ARCHITECTURE & ABSTRACTION HIERARCHY", fill=(248, 250, 252), font=fonts["header"])
    draw.text((64, 88), "CompTIA Tech+ FC0-U71: How Applications, Shell, Kernel, Drivers, and Hardware interact through Privileged Rings", fill=(148, 163, 184), font=fonts["subhdr"])

    # Colors
    c_user = {"bg": (16, 26, 44, 250), "border": (56, 189, 248, 255), "accent": (56, 189, 248, 255)}
    c_gate = {"bg": (38, 22, 10, 250), "border": (251, 146, 60, 255), "accent": (251, 146, 60, 255)}
    c_kernel = {"bg": (34, 16, 44, 250), "border": (192, 132, 252, 255), "accent": (192, 132, 252, 255)}
    c_driver = {"bg": (12, 36, 28, 250), "border": (52, 211, 153, 255), "accent": (52, 211, 153, 255)}
    c_hw = {"bg": (22, 26, 38, 250), "border": (148, 163, 184, 255), "accent": (148, 163, 184, 255)}

    # Tier 1: USER MODE / RING 3 (Top)
    t1_y = 150
    t1_h = 240
    draw.rounded_rectangle([60, t1_y, 2440, t1_y + t1_h], radius=14, fill=c_user["bg"], outline=c_user["border"], width=2)
    # Badge
    draw.rounded_rectangle([80, t1_y + 16, 80 + 200, t1_y + 16 + 24], radius=6, fill=c_user["accent"])
    draw.text((90, t1_y + 18), "USER SPACE (RING 3)", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((300, t1_y + 16), "Unprivileged execution mode — programs cannot touch memory or hardware directly", fill=(148, 163, 184), font=fonts["subhdr"])

    # 3 Sub-blocks in User Space
    sub_w = 750
    sub_h = 150
    sub_y = t1_y + 65

    # Sub 1A: User Applications
    draw.rounded_rectangle([80, sub_y, 80 + sub_w, sub_y + sub_h], radius=10, fill=(11, 18, 32), outline=(56, 189, 248, 100), width=1)
    draw.text((100, sub_y + 12), "User Applications & Binaries", fill=(248, 250, 252), font=fonts["box_title"])
    draw.text((100, sub_y + 42), "• Productivity: Office 365, LibreOffice, Document Editors", fill=(203, 213, 225), font=fonts["body"])
    draw.text((100, sub_y + 72), "• Web Browsers: Chrome, Firefox, Safari (isolated sandboxes)", fill=(203, 213, 225), font=fonts["body"])
    draw.text((100, sub_y + 102), "• Databases & Games: Client applications, development IDEs", fill=(203, 213, 225), font=fonts["body"])

    # Sub 1B: User Shell & Interface
    draw.rounded_rectangle([865, sub_y, 865 + sub_w, sub_y + sub_h], radius=10, fill=(11, 18, 32), outline=(56, 189, 248, 100), width=1)
    draw.text((885, sub_y + 12), "The Shell: User Interaction Layer", fill=(248, 250, 252), font=fonts["box_title"])
    draw.text((885, sub_y + 42), "• GUI (Graphical User Interface): Windows Desktop, macOS Aqua", fill=(203, 213, 225), font=fonts["body"])
    draw.text((885, sub_y + 72), "• CLI (Command Line Interface): Bash, Zsh, PowerShell, Command Prompt", fill=(203, 213, 225), font=fonts["body"])
    draw.text((885, sub_y + 102), "• Function: Interprets human commands and launches executable processes", fill=(203, 213, 225), font=fonts["body"])

    # Sub 1C: System Daemons & Services
    draw.rounded_rectangle([1650, sub_y, 1650 + sub_w, sub_y + sub_h], radius=10, fill=(11, 18, 32), outline=(56, 189, 248, 100), width=1)
    draw.text((1670, sub_y + 12), "Background Daemons & Services", fill=(248, 250, 252), font=fonts["box_title"])
    draw.text((1670, sub_y + 42), "• Windows Services / Linux Daemons: sshd, print spooler, audio engine", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1670, sub_y + 72), "• Automation: Scheduled tasks, monitoring agents, update services", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1670, sub_y + 102), "• Execution: Runs silently without active user interface session", fill=(203, 213, 225), font=fonts["body"])

    # Tier 2: SYSTEM CALL INTERFACE (Syscall Boundary)
    t2_y = 425
    t2_h = 70
    draw.rounded_rectangle([60, t2_y, 2440, t2_y + t2_h], radius=10, fill=c_gate["bg"], outline=c_gate["border"], width=2)
    draw.text((90, t2_y + 22), "SYSTEM CALL INTERFACE (SYSCALLS)", fill=c_gate["accent"], font=fonts["tier_title"])
    draw.text((490, t2_y + 24), "The Secure Bridge: Controlled Context Switch from Ring 3 (User) to Ring 0 (Kernel) via software interrupts [ read(), write(), open(), fork(), socket() ]", fill=(248, 250, 252), font=fonts["gate"])

    # Arrows indicating down transition
    draw.polygon([(1250, 410), (1240, 395), (1260, 395)], fill=(251, 146, 60, 255))
    draw.polygon([(1250, 510), (1240, 495), (1260, 495)], fill=(251, 146, 60, 255))

    # Tier 3: KERNEL SPACE / RING 0 (Core OS)
    t3_y = 525
    t3_h = 360
    draw.rounded_rectangle([60, t3_y, 2440, t3_y + t3_h], radius=14, fill=c_kernel["bg"], outline=c_kernel["border"], width=2)
    # Badge
    draw.rounded_rectangle([80, t3_y + 16, 80 + 230, t3_y + 16 + 24], radius=6, fill=c_kernel["accent"])
    draw.text((90, t3_y + 18), "THE KERNEL (RING 0 SUPERVISOR)", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((330, t3_y + 16), "The core engine of the operating system: runs in privileged mode with complete control over physical hardware", fill=(148, 163, 184), font=fonts["subhdr"])

    # 4 Kernel Core Subsystems
    k_w = 560
    k_h = 265
    k_y = t3_y + 65

    # K1: Process Scheduler
    draw.rounded_rectangle([80, k_y, 80 + k_w, k_y + k_h], radius=10, fill=(20, 12, 30), outline=(192, 132, 252, 120), width=1)
    draw.text((100, k_y + 14), "1. Process Scheduler", fill=(248, 250, 252), font=fonts["box_title"])
    draw.text((100, k_y + 44), "• Preemptive Multitasking:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((100, k_y + 70), "  Allocates millisecond CPU time-slices", fill=(203, 213, 225), font=fonts["body"])
    draw.text((100, k_y + 96), "  across all active system threads.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((100, k_y + 130), "• Priority Scheduling:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((100, k_y + 156), "  Critical OS tasks preempt user programs.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((100, k_y + 190), "• Core Affinity:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((100, k_y + 216), "  Balances workload across multi-core CPUs.", fill=(203, 213, 225), font=fonts["body"])

    # K2: Memory Manager
    draw.rounded_rectangle([670, k_y, 670 + k_w, k_y + k_h], radius=10, fill=(20, 12, 30), outline=(192, 132, 252, 120), width=1)
    draw.text((690, k_y + 14), "2. Memory Manager (VMM)", fill=(248, 250, 252), font=fonts["box_title"])
    draw.text((690, k_y + 44), "• Virtual Memory Mapping:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((690, k_y + 70), "  Translates virtual program addresses to", fill=(203, 213, 225), font=fonts["body"])
    draw.text((690, k_y + 96), "  physical DDR5 RAM addresses via MMU.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((690, k_y + 130), "• Process Isolation:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((690, k_y + 156), "  Prevents App A from reading App B memory.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((690, k_y + 190), "• Paging & Swap Space:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((690, k_y + 216), "  Pages idle memory blocks to NVMe disk.", fill=(203, 213, 225), font=fonts["body"])

    # K3: File System & I/O
    draw.rounded_rectangle([1260, k_y, 1260 + k_w, k_y + k_h], radius=10, fill=(20, 12, 30), outline=(192, 132, 252, 120), width=1)
    draw.text((1280, k_y + 14), "3. Virtual File System (VFS)", fill=(248, 250, 252), font=fonts["box_title"])
    draw.text((1280, k_y + 44), "• Uniform Abstraction:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((1280, k_y + 70), "  Standardizes file access whether on", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1280, k_y + 96), "  NTFS, ext4, APFS, or network shares.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1280, k_y + 130), "• Metadata & Permissions:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((1280, k_y + 156), "  Enforces file ownership, ACLs, & timestamps.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1280, k_y + 190), "• Disk Buffer Cache:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((1280, k_y + 216), "  Caches read blocks in RAM for fast access.", fill=(203, 213, 225), font=fonts["body"])

    # K4: Security & Network Stack
    draw.rounded_rectangle([1850, k_y, 1850 + k_w, k_y + k_h], radius=10, fill=(20, 12, 30), outline=(192, 132, 252, 120), width=1)
    draw.text((1870, k_y + 14), "4. Security & Network Stack", fill=(248, 250, 252), font=fonts["box_title"])
    draw.text((1870, k_y + 44), "• TCP/IP Protocol Engine:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((1870, k_y + 70), "  Packet encapsulation, routing, sockets.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1870, k_y + 96), "• Access Control & Tokens:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((1870, k_y + 122), "  Validates user SID tokens & privileges.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1870, k_y + 156), "• Kernel Firewalling:", fill=(192, 132, 252), font=fonts["body_bold"])
    draw.text((1870, k_y + 182), "  Stateful packet filtering & NAT translation.", fill=(203, 213, 225), font=fonts["body"])
    draw.text((1870, k_y + 216), "• Crash Guard (BSOD/Panic):", fill=(244, 63, 94), font=fonts["body_bold"])

    # Tier 4: DEVICE DRIVERS & HARDWARE ABSTRACTION LAYER (HAL)
    t4_y = 920
    t4_h = 175
    draw.rounded_rectangle([60, t4_y, 2440, t4_y + t4_h], radius=14, fill=c_driver["bg"], outline=c_driver["border"], width=2)
    # Badge
    draw.rounded_rectangle([80, t4_y + 16, 80 + 260, t4_y + 16 + 24], radius=6, fill=c_driver["accent"])
    draw.text((90, t4_y + 18), "DEVICE DRIVERS & HAL LAYER", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((360, t4_y + 16), "Hardware Abstraction: Translates generic OS operations into device-specific silicon commands", fill=(148, 163, 184), font=fonts["subhdr"])

    d_w = 560
    d_h = 95
    d_y = t4_y + 55
    d_boxes = [
        (80, "Storage Controller Drivers", "NVMe PCIe Driver · AHCI SATA Driver · USB Mass Storage"),
        (670, "Graphics Display Drivers", "NVIDIA/AMD/Intel GPU Kernel Mode Driver (DirectX / Vulkan)"),
        (1260, "Network Interface Drivers", "Gigabit Ethernet NIC Driver · Wi-Fi 6E/7 Wireless PHY Driver"),
        (1850, "Chipset & Bus Drivers", "PCI Express Root Complex · USB Host Controller · ACPI Power"),
    ]
    for bx, btitle, bdesc in d_boxes:
        draw.rounded_rectangle([bx, d_y, bx + d_w, d_y + d_h], radius=8, fill=(10, 24, 18), outline=(52, 211, 153, 100), width=1)
        draw.text((bx + 16, d_y + 12), btitle, fill=(248, 250, 252), font=fonts["box_title"])
        draw.text((bx + 16, d_y + 44), bdesc, fill=(203, 213, 225), font=fonts["body"])

    # Tier 5: PHYSICAL HARDWARE (Silicon)
    t5_y = 1130
    t5_h = 220
    draw.rounded_rectangle([60, t5_y, 2440, t5_y + t5_h], radius=14, fill=c_hw["bg"], outline=c_hw["border"], width=2)
    # Badge
    draw.rounded_rectangle([80, t5_y + 16, 80 + 200, t5_y + 16 + 24], radius=6, fill=c_hw["accent"])
    draw.text((90, t5_y + 18), "PHYSICAL HARDWARE", fill=(10, 15, 29), font=fonts["badge"])
    draw.text((300, t5_y + 16), "The actual silicon: executes machine code instructions and stores digital voltage states", fill=(148, 163, 184), font=fonts["subhdr"])

    h_w = 440
    h_h = 130
    h_y = t5_y + 58
    h_items = [
        (80, "CPU Microprocessor", "x86-64 / ARM64\nRegisters · L1/L2/L3 Cache\nALU Execution Units"),
        (550, "System Memory", "DDR4 / DDR5 RAM\nVolatile High-Speed Storage\nMemory Bus Interface"),
        (1020, "Non-Volatile Storage", "M.2 NVMe PCIe SSD\nSATA Solid-State Drive\nMechanical Hard Disk Drive"),
        (1490, "Expansion & Graphics", "Discrete Graphics Card (GPU)\nPCIe 5.0 High-Speed Lanes\nDedicated VRAM Buffer"),
        (1960, "Network & Peripherals", "RJ-45 Ethernet Port\nWi-Fi Antennas & Bluetooth\nUSB Controllers & Audio DAC"),
    ]
    for bx, btitle, bdesc in h_items:
        draw.rounded_rectangle([bx, h_y, bx + h_w, h_y + h_h], radius=8, fill=(16, 20, 30), outline=(148, 163, 184, 100), width=1)
        draw.text((bx + 16, h_y + 12), btitle, fill=(248, 250, 252), font=fonts["box_title"])
        lines = bdesc.split("\n")
        ly = h_y + 42
        for l in lines:
            draw.text((bx + 16, ly), l, fill=(203, 213, 225), font=fonts["body"])
            ly += 26

    final_img = Image.alpha_composite(img, overlay).convert("RGB")
    final_img.save(out_path, quality=95)
    print(f"Generated OS architecture diagram to {out_path}")

if __name__ == "__main__":
    generate_os_architecture_diagram("public/images/tech-plus/os-architecture-kernel-shell-hardware.jpg")
