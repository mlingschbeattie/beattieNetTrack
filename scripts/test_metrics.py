from PIL import ImageDraw, ImageFont, Image

f_title = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 26)
f_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 19)
f_badge = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
img = Image.new('RGB', (100, 100))
d = ImageDraw.Draw(img)

titles = [
    '8+8 Pin CPU Power (EPS 12V)',
    'CPU Socket (LGA 1700)',
    'Rear I/O External Ports',
    'PCIe Expansion Slots (x1 / x4)',
    'Front Panel Audio & USB Headers',
    'DDR5 Memory Slots (DIMM 1-4)',
    '24-Pin ATX Main Power Header',
    'M.2 NVMe PCIe SSD Slot (Gen 5)',
    'PCIe 5.0 x16 Slot (Steel Armor)',
    'SATA 6Gbps Storage Ports',
    'Front Panel Switch/LED Header'
]

subs = [
    'Plugs: Dedicated 8-Pin CPU 12V power cables from PSU',
    'Plugs: Processor (Intel Core 12th-14th Gen) under ZIF lever',
    'Plugs: Monitors (DP/HDMI), 2.5GbE LAN, USB, Audio',
    'Plugs: Add-in cards (Wi-Fi, 10GbE NICs, Sound, Capture)',
    'Plugs: Case Front USB 2.0/3.2 and HD Audio cables',
    'Plugs: System RAM sticks (Dual-Channel Priority A2/B2)',
    'Plugs: Main 24-Pin harness from PSU (powers board & chipset)',
    'Plugs: High-speed M.2 2280 NVMe SSD (under heatsink)',
    'Plugs: Dedicated Graphics Card (Discrete GPU)',
    'Plugs: SATA Data cables to 2.5" SSDs & 3.5" Hard Drives',
    'Plugs: Case Power Switch, Reset Button, HDD & Power LEDs'
]

max_t = max(d.textlength(t, font=f_title) for t in titles)
max_s = max(d.textlength(s, font=f_sub) for s in subs)
badge_w = max(d.textlength(cat, font=f_badge) for cat in ['COMPUTE', 'POWER', 'GPU', 'STORAGE', 'IO', 'EXPANSION', 'CHASSIS'])

print(f'Max title width: {max_t:.1f}px')
print(f'Max subtitle width: {max_s:.1f}px')
print(f'Max badge width: {badge_w:.1f}px')
