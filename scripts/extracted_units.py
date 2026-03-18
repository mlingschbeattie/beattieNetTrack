# ── EXTRACTED UNITS ─────────────────────────────────────────────────
# Paste these entries INSIDE the UNITS dict in make_resource_pdfs.py
# Review titles, objective codes, and question formatting before use.
# ─────────────────────────────────────────────────────────────────────

    "1.2.1": {
        "unit": "1.2.1",
        "title": "Network Topologies",
        "n10_009": "1.2",
        "n10_008": "1.2",
        "questions": [
            {
                "num": "1",
                "question": "In a _______ topology, all devices connect to a single shared cable called a _______. If that cable fails\n    at any point, _______ devices lose connectivity.",
                "answer": "Bus; backbone; all.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A ring topology passes a special _______ frame around the loop to control who can transmit. The main\n    weakness of a single-ring design is that one _______ or _______ failure breaks the entire loop.",
                "answer": "Token; device; cable segment.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "In a star topology, all devices connect to a central _______. A single device failure affects only\n    _______ device. The central device, however, is a _______ — if it fails, the entire segment goes down.",
                "answer": "Switch (or hub); that one; single point of failure.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "In a full mesh topology with 10 devices, how many point-to-point links are required? Show the formula\n    and the result.",
                "answer": "Formula: n(n-1)/2. With n=10: 10 × 9 / 2 = 45 links.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Explain the difference between a full mesh and a partial mesh. Why is partial mesh the more common\n    real-world design?",
                "answer": "Full mesh connects every device to every other device — maximum redundancy but exponential cost. Partial mesh only gives multiple connections to critical devices. Real-world networks use partial mesh because full mesh becomes prohibitively expensive at scale.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "_______ topology combines two or more topology types. Give one real-world example: _______.",
                "answer": "Hybrid; e.g., star topology inside each building connected by a partial mesh WAN between buildings (or similar valid example).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Physical topology is the _______ layout of cables and devices. Logical topology is the path _______\n    actually takes. These two can differ — give an example of when they do.",
                "answer": "Actual physical; data. Example: Token Ring physically wired as a star through a MAU, but data travels logically in a ring. Or: two devices on the same physical switch but on different VLANs are logically on separate networks.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: An entire floor of a building loses network access simultaneously. No individual device\n    issues are reported. Based on what you know about network topologies, what topology is most likely in\n    use, what single component probably failed, and what design change would prevent this from\n    happening again?",
                "answer": "Star topology is almost certainly in use — one switch failure taking down all devices is the classic star failure mode. The access-layer switch lost power or hardware failed. Prevention: add a redundant switch in a stacked or dual-uplink configuration, use a managed switch with dual power supplies, or implement a two-tier design where devices connect to a redundant distribution layer.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.2.2": {
        "unit": "1.2.2",
        "title": "Network Types",
        "n10_009": "1.2",
        "n10_008": "1.2",
        "questions": [
            {
                "num": "1",
                "question": "A _______ (LAN) covers a single building or small group of buildings and is typically owned by\n    _______. A _______ (WAN) connects networks across large geographic distances and usually crosses\n    infrastructure owned by _______.",
                "answer": "Local Area Network; the organization; Wide Area Network; carriers or ISPs.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Match each network type to its scope:\n    Personal Area Network (PAN) ﬁ _______\n    Campus Area Network (CAN) ﬁ _______\n    Metropolitan Area Network (MAN) ﬁ _______",
                "answer": "PAN ﬁ ~1 meter, personal devices (Bluetooth, NFC); CAN ﬁ multiple buildings on a defined campus; MAN ﬁ city or large district.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "A WLAN provides the same connectivity as a wired LAN but uses _______ instead of copper or fiber.\n    Two key tradeoffs versus wired Ethernet are _______ and _______.",
                "answer": "Radio frequencies (802.11/Wi-Fi); shared medium / half-duplex performance; inherently less secure (signal is not contained inside a cable). Also acceptable: signal degradation with distance.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "MPLS routes WAN traffic using short _______ instead of full IP addresses. Businesses buy MPLS\n    circuits for _______ and _______. The main disadvantage of MPLS compared to newer options is\n    _______.",
                "answer": "Path labels; guaranteed bandwidth (SLAs); predictable performance. Main disadvantage: high cost.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "SD-WAN places a _______ layer on top of multiple transport links (MPLS, broadband, LTE) and routes\n    traffic based on _______. The business benefit over traditional MPLS is _______.",
                "answer": "Software; real-time performance metrics; lower cost — commodity internet links can replace or supplement expensive MPLS circuits while maintaining application-aware routing.",
                "lines": 4
            },
            {
                "num": "6",
                "question": "In a _______ network architecture, dedicated servers provide resources and clients consume them. In\n    a _______ architecture, every device can act as both client and server. At approximately _______\n    devices, peer-to-peer becomes unmanageable.\n    Answer: Client-server; peer-to-peer (P2P); 10 devices.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A SOHO network is typically a _______ design with one _______ and one _______ domain. The\n    all-in-one device combines a router, switch, wireless access point, DHCP server, firewall, and _______\n    in a single box.",
                "answer": "Flat; subnet; broadcast; NAT gateway.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school's IoT security cameras have been compromised and are sending spam traffic.\n    The cameras share the same network as student workstations and staff file servers. What network\n    design change would contain the damage and prevent the cameras from reaching production systems?\n    Explain the concept behind your solution.",
                "answer": "Segment the IoT devices onto a separate VLAN or subnet, isolated from the production LAN. A compromised device on a different VLAN cannot reach the file server without traffic crossing a router, where a firewall policy can block it. Best practice: IoT VLAN with a deny-all-to-production rule, allowing only necessary outbound internet traffic for device management.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.3.1": {
        "unit": "1.3.1",
        "title": "Copper Cables",
        "n10_009": "1.3",
        "n10_008": "1.3",
        "questions": [
            {
                "num": "1",
                "question": "The standard Ethernet cable used in most LANs is _______ (UTP/STP). The engineering trick that\n    cancels out EMI inside this cable is the _______ of the wire pairs.",
                "answer": "UTP (Unshielded Twisted Pair); twist.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Match each cable category to its maximum speed at 100 meters:\n    Cat5e ﬁ _______\n    Cat6 ﬁ _______ (at 100m) / _______ (at 55m)\n    Cat6a ﬁ _______",
                "answer": "Cat5e ﬁ 1 Gbps; Cat6 ﬁ 1 Gbps at 100m / 10 Gbps at 55m; Cat6a ﬁ 10 Gbps.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Cat8 supports speeds of _______ Gbps but is limited to _______ meters. It is designed for _______\n    environments, not workstation drops.",
                "answer": "25 or 40 Gbps; 30 meters; data center.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Coaxial cable carries broadband internet from the ISP to the cable modem using the _______ standard.\n    In data centers, a two-conductor variant called _______ cable is used for short high-speed switch\n    connections.",
                "answer": "DOCSIS; twinaxial (DAC).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "List the three jacket ratings from most to least restrictive and describe where each must be used:\n    1. _______\n    2. _______\n    3. _______",
                "answer": "1. Plenum — above drop ceilings and below raised floors (air handling spaces); 2. Riser — vertical runs between floors; 3. PVC — open areas and surface-mounted runs only.",
                "lines": 4
            },
            {
                "num": "6",
                "question": "A straight-through cable connects _______ devices (e.g., PC to switch). A crossover cable connects\n    _______ devices (e.g., switch to switch). A rollover/console cable reverses all _______ pins and is\n    used to connect a laptop to a device's _______ port.",
                "answer": "Unlike; like; eight; console.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The maximum copper Ethernet segment length is _______ meters total. The TIA/EIA standard budgets\n    _______ meters for the permanent link and _______ meters for patch cables. If a run exceeds this limit,\n    the two options are _______.",
                "answer": "100 meters; 90 meters; 10 meters; add a switch in the middle or switch to fiber.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user reports their workstation connects at 100 Mbps instead of 1 Gbps. The cable\n    run is 85 meters and passes near fluorescent light fixtures for about 20 feet. What are the two most\n    likely causes and how would you confirm each?",
                "answer": "1. Physical damage/kink — inspect visually and test with a cable certifier; a damaged pair shows as a wire map or attenuation failure. 2. EMI from fluorescent ballasts — reroute the cable or replace with STP; a cable certifier running NEXT tests will show elevated noise if EMI is the cause.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.3.2": {
        "unit": "1.3.2",
        "title": "Fiber Optic Cables",
        "n10_009": "1.3",
        "n10_008": "1.3",
        "questions": [
            {
                "num": "1",
                "question": "Fiber-optic cable transmits data as pulses of _______ instead of electrical signals. This makes it\n    immune to _______ and safe to run between buildings without risk of _______.",
                "answer": "Light; electromagnetic interference (EMI); ground loops or lightning damage.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Multimode fiber has a _______ (larger/smaller) core than single-mode. Its light source is a _______,\n    which is cheaper than the _______ used in single-mode. The main distance limitation of multimode is\n    caused by _______.",
                "answer": "Larger; LED; laser; modal dispersion.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Single-mode fiber has a core of approximately _______ microns and supports runs of up to _______\n    km without a repeater. Its jacket color is _______. Multimode jacket colors are _______ or _______.",
                "answer": "8-9 microns; 80 km; yellow; orange or aqua.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Match each fiber connector to its description:\n    SC ﬁ _______\n    LC ﬁ _______\n    ST ﬁ _______",
                "answer": "SC ﬁ square, push-pull, found on older installations; LC ﬁ small form-factor, latch clip, dominates modern SFP/SFP+ installations; ST ﬁ round, bayonet twist-lock, legacy multimode.",
                "lines": 4
            },
            {
                "num": "5",
                "question": "Fiber connections always come in pairs because one strand _______ and the other _______.\n    Swapping these two strands is a common mistake that mixes up _______ and _______.",
                "answer": "Transmits; receives; TX; RX.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "UPC connectors have a _______ housing. APC connectors have a _______ housing and polish the\n    endface at a _______ angle. These two types are physically _______ and must never be mated.",
                "answer": "Blue; green; 8-degree; incompatible.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Exceeding a fiber cable's minimum _______ causes macrobending loss. Contaminated fiber endfaces\n    must be cleaned with _______ before every connection. Unused connectors and ports should always\n    be _______.",
                "answer": "Bend radius; lint-free wipes and isopropyl alcohol (or one-click cleaners); capped.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A backbone fiber link between two wiring closets starts throwing CRC errors and\n    negotiates at a lower speed. Both ends use LC connectors with blue boots. Walk through your\n    troubleshooting steps in order.",
                "answer": "1. Inspect run for bend radius violations. 2. Clean both endfaces with a one-click cleaner or lint-free wipe + IPA. 3. Use a fiber light meter to check power levels at the receive end. 4. Inspect connectors under a fiber microscope for contamination or damage. 5. Confirm both are UPC (blue = correct). 6. Test with a known-good patch cable to isolate permanent link vs patch.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.3.3": {
        "unit": "1.3.3",
        "title": "Connector Types",
        "n10_009": "1.3",
        "n10_008": "1.3",
        "questions": [
            {
                "num": "1",
                "question": "RJ-45 has _______ pins and is used for _______. RJ-11 has _______ positions and is used for\n    _______. The key physical difference is _______.",
                "answer": "8 pins; Ethernet; 6 positions; telephone/DSL; RJ-11 is noticeably narrower with fewer visible contacts.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "BNC connectors use a _______ locking mechanism and were used for _______ Ethernet. F-type\n    connectors use _______ and are found on _______.",
                "answer": "Bayonet twist-lock; 10BASE2 (Thinnet); threading; cable modems and DOCSIS broadband installations.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Match each fiber connector to its physical description and status:\n    LC ﬁ _______\n    SC ﬁ _______\n    ST ﬁ _______",
                "answer": "LC ﬁ small, rectangular, spring-loaded latch, modern standard for SFP/SFP+; SC ﬁ larger, square, push-pull, found on older/legacy installations; ST ﬁ round, bayonet twist-lock, legacy 1990s multimode installations.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "An MPO/MTP connector carries _______, _______, or _______ fibers in a single housing. It is used in\n    _______ environments where running individual fiber patch cables for every connection is impractical.",
                "answer": "8, 12, or 24 fibers; data center.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "DB-9 is a _______ pin serial connector used for _______ access to network devices. It works even\n    when the network is completely down because it is _______ access. Modern laptops require a _______\n    adapter to use it.",
                "answer": "9-pin; console (out-of-band); out-of-band; USB-to-DB-9.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "SFP supports up to _______ Gbps. SFP+ supports up to _______ Gbps. QSFP+ supports up to\n    _______ Gbps. The advantage of SFP-style ports over fixed ports is _______.",
                "answer": "1 Gbps; 10 Gbps; 40 Gbps; modularity — the same port can accept different transceivers for different media types (fiber or copper, different distances).",
                "lines": 4
            },
            {
                "num": "7",
                "question": "PoE (Power over Ethernet) uses _______ connectors to deliver both _______ and _______ over the\n    same cable to devices like _______, _______, and _______.",
                "answer": "RJ-45; DC power; data; access points, IP phones, security cameras (any three).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: You're setting up a new switch with SFP+ ports. You need to connect it to two devices:\n    one 60 meters away over existing multimode fiber, and one directly adjacent in the same rack. What\n    transceiver type do you order for each connection and why?",
                "answer": "60m multimode fiber ﬁ SFP+ multimode fiber transceiver (LC connector, 850nm, OM3/OM4 rated for 10GBase-SR). Adjacent rack connection ﬁ SFP+ DAC (Direct Attach Copper) twinaxial cable, which is cheaper than a transceiver pair for very short distances and avoids the need for patch cables entirely.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "1.3.4": {
        "unit": "1.3.4",
        "title": "Cable Management",
        "n10_009": "1.3",
        "n10_008": "1.3",
        "questions": [
            {
                "num": "1",
                "question": "A patch panel is a _______ device (active/passive) that terminates _______ cable runs on its back side\n    using a _______ tool, and provides _______ ports on its front side for connecting to switches.",
                "answer": "Passive; permanent horizontal; 110-style punch-down; RJ-45.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The key benefit of using a patch panel is the separation between _______ infrastructure and _______\n    equipment. To move a user to a different switch port, you only need to move the _______ — the cable\n    in the wall never changes.",
                "answer": "Permanent (horizontal) infrastructure; active switching equipment; patch cable on the front of the panel.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "_______ cable managers mount between devices in a rack to route patch cables side to side. _______\n    cable managers run along the sides of the rack to contain bulk cables from top to bottom. _______ are\n    open or enclosed metal troughs in ceilings or raised floors that support horizontal cable runs.",
                "answer": "Horizontal; vertical; cable trays.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Explain why zip ties should NOT be used on data cable bundles, and what should be used instead.",
                "answer": "Over-tightened zip ties deform the cable jacket and change the geometry of the twisted pairs inside, causing crosstalk and attenuation that may not appear immediately but develops over time. Velcro (hook-and-loop) straps should be used instead — they hold firmly without crushing the cable and can be reopened when cables are added or removed.",
                "lines": 6
            },
            {
                "num": "5",
                "question": "When installing a cable drop to Room 214, outlet A, what three things get labeled '214-A'?\n    1. _______\n    2. _______\n    3. _______",
                "answer": "1. The wall jack in Room 214; 2. The corresponding patch panel port; 3. Both ends of the cable run in the ceiling.",
                "lines": 4
            },
            {
                "num": "6",
                "question": "One rack unit (1U) equals _______ inches. A standard full-height rack is _______ U. Heavy equipment\n    such as _______ should be mounted at the _______ of the rack for stability. Racks should be left\n    _______ % empty for future expansion.\n    Answer: 1.75 inches; 42U; UPS units; bottom; 20-30%.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The _______ standard defines labeling conventions for commercial cabling systems. Network\n    documentation should be stored _______ (location), not in one person's head, and must include at\n    minimum: _______, _______, and _______.",
                "answer": "TIA-606; in a shared location accessible to the whole team (wiki, NMS, shared drive); physical layer diagram, logical diagram with VLAN/switch port assignments, and a change log.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: You're handed a network closet that has no labels, cables draped over equipment, and\n    no documentation. You need to find which patch panel port connects to a specific classroom without\n    taking the network down. Describe your approach step by step.",
                "answer": "1. Get a cable toner/tracer — tone the wall jack in the classroom and trace the tone to the patch panel to identify the port. 2. Label that port immediately. 3. Check which switch port it patches to and document that mapping. 4. Repeat for all active ports, building a port-to-room map as you go. 5. Once all active ports are mapped, create printed labels for the panel and a physical diagram. Document in a shared location before leaving the closet.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "1.4.1": {
        "unit": "1.4.1",
        "title": "Public Private Networks",
        "n10_009": "1.4",
        "n10_008": "1.4",
        "questions": [
            {
                "num": "1",
                "question": "List the three RFC 1918 private IP ranges and their CIDR notation:\n    1. _______ (_______)\n    2. _______ (_______)\n    3. _______ (_______)",
                "answer": "1. 10.0.0.0 – 10.255.255.255 (10.0.0.0/8); 2. 172.16.0.0 – 172.31.255.255 (172.16.0.0/12); 3. 192.168.0.0 – 192.168.255.255 (192.168.0.0/16).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Private IP addresses are never _______ on the public internet. The reason private addressing exists is\n    that IPv4 only provides approximately _______ total addresses, which is not enough for every device in\n    the world to have a unique public IP.",
                "answer": "Routed; 4.3 billion.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "NAT stands for _______. When a device on a private network sends traffic to the internet, the router\n    replaces the _______ IP with its own _______ IP before forwarding the packet.",
                "answer": "Network Address Translation; private source; public.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "PAT (Port Address Translation) allows an entire network to share a _______ public IP address. It tracks\n    which internal device made which request by assigning unique _______ numbers to each outbound\n    connection.",
                "answer": "Single; source port.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "APIPA assigns addresses in the _______ range when a device cannot reach a _______. An APIPA\n    address means the device can only communicate with _______ on the same segment and cannot\n    reach _______.",
                "answer": "169.254.0.0/16; DHCP server; other APIPA devices; any gateway or remote network.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "When a technician sees a 169.254.x.x address on a workstation, list three things they should\n    immediately check:\n    1. _______\n    2. _______\n    3. _______\n    Answer: 1. Is the DHCP server running? 2. Is the DHCP scope exhausted (out of addresses)? 3. Is the\n    network cable connected / is there a link? (Any three valid checks.)",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The loopback address is _______. Pinging this address tests whether _______ is functioning on the\n    local machine. Traffic sent to this address never leaves the device and never touches _______.",
                "answer": "127.0.0.1; the TCP/IP stack; a cable or NIC.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user calls to say they can't access anything on the network or the internet. You\n    remotely view their screen and see their IP address is 169.254.83.42. Walk through your diagnostic\n    steps in order.",
                "answer": "1. Confirm APIPA — DHCP failed. 2. Check physical connection (cable seated, link light on). 3. Try to ping the DHCP server by IP from another device to confirm it's reachable. 4. Check if DHCP service is running on the server. 5. Check if the DHCP scope is exhausted. 6. If physical and server are fine, try ipconfig /release and /renew to force a new DHCP request. 7. If still failing, check switch port, VLAN assignment, and DHCP relay/helper address configuration.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "1.4.2": {
        "unit": "1.4.2",
        "title": "Ipv4 Ipv6",
        "n10_009": "1.4",
        "n10_008": "1.4",
        "questions": [
            {
                "num": "1",
                "question": "An IPv4 address is _______ bits long, written as _______ octets in dotted decimal notation. Each octet\n    ranges from _______ to _______. The total number of possible IPv4 addresses is approximately\n    _______.",
                "answer": "32 bits; four; 0; 255; 4.3 billion.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Every IPv4 address has two parts: a _______ portion and a _______ portion. The _______ determines\n    where the split falls. A /24 mask means _______ bits are network and _______ bits are host.",
                "answer": "Network; host; subnet mask; 24 bits; 8 bits.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "CIDR notation /30 leaves _______ bits for hosts, providing _______ total addresses and _______\n    usable addresses. This is typically used for _______.",
                "answer": "2 bits; 4 total addresses; 2 usable; point-to-point links between two routers.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "IPv6 addresses are _______ bits long, written as _______ groups of _______ hexadecimal digits\n    separated by colons. Two shorthand rules are: (1) _______ and (2) _______.",
                "answer": "128 bits; eight groups; four hex digits; leading zeros in any group can be dropped; one consecutive span of all-zero groups can be replaced with :: (double colon, used only once per address).",
                "lines": 5
            },
            {
                "num": "5",
                "question": "A standard IPv6 subnet assignment uses a _______ prefix, giving _______ bits for the host identifier.\n    Devices can generate their own host portion automatically using _______ (SLAAC) without needing a\n    DHCP server.",
                "answer": "/64; 64 bits; Stateless Address Autoconfiguration.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "IPv6 has NO _______ addresses. Instead it uses three communication types:\n    _______ — one to one\n    _______ — one to many (replaces broadcast functions)\n    _______ — one to nearest",
                "answer": "Broadcast; unicast; multicast; anycast.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Match each IPv6 address prefix to its type:\n    fe80::/10 ﬁ _______\n    2000::/3 ﬁ _______\n    ff00::/8 ﬁ _______",
                "answer": "fe80::/10 ﬁ link-local unicast; 2000::/3 ﬁ global unicast (public, internet-routable); ff00::/8 ﬁ multicast.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: You run ipconfig on a Windows workstation and see both a 192.168.1.45 address and\n    a 2001:db8::42 address on the same adapter. What is this configuration called, and what does it mean\n    for how the machine connects to the internet?",
                "answer": "This is dual-stack. The machine has both IPv4 and IPv6 addresses active simultaneously. The OS will prefer IPv6 for connections to destinations that support it, and fall back to IPv4 for destinations that don't. Both protocols are fully functional — it's not a misconfiguration, it's the standard transition approach while the internet completes its migration to IPv6.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.5.1": {
        "unit": "1.5.1",
        "title": "Common Ports",
        "n10_009": "1.5",
        "n10_008": "1.5",
        "questions": [
            {
                "num": "1",
                "question": "Ports are _______ -bit numbers ranging from _______ to _______. The three ranges are:\n    Well-known: _______\n    Registered: _______\n    Dynamic/Ephemeral: _______",
                "answer": "16-bit; 0; 65535. Well-known: 0-1023; Registered: 1024-49151; Dynamic/Ephemeral: 49152-65535.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Fill in the port numbers:\n    FTP control / data ﬁ _______ / _______\n    SSH ﬁ _______\n    Telnet ﬁ _______\n    SMTP ﬁ _______\n    DNS ﬁ _______",
                "answer": "FTP: 21 (control) / 20 (data); SSH: 22; Telnet: 23; SMTP: 25; DNS: 53.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Fill in the port numbers:\n    DHCP server / client ﬁ _______ / _______\n    HTTP ﬁ _______\n    HTTPS ﬁ _______\n    SMB ﬁ _______\n    RDP ﬁ _______",
                "answer": "DHCP: 67 (server) / 68 (client); HTTP: 80; HTTPS: 443; SMB: 445; RDP: 3389.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "FTP transmits credentials in _______. Its secure replacements are _______ (runs over SSH, port 22)\n    and _______ (FTP over TLS). Telnet is similarly insecure because _______.",
                "answer": "Plaintext; SFTP; FTPS; all traffic including passwords travels unencrypted.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "DNS normally uses _______ (TCP/UDP) on port 53 for standard queries because _______. It switches\n    to _______ for zone transfers and large responses because _______.",
                "answer": "UDP; it's faster for small single request-response lookups; TCP; reliability is needed for larger transfers.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "When your browser connects to a web server on port 443, your OS assigns a temporary _______ port\n    (range: _______) as the source port. This port exists only for the duration of that _______.",
                "answer": "Ephemeral; 49152-65535; connection/session.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "SMB uses port _______. The _______ ransomware in 2017 exploited a vulnerability in SMB version\n    _______, which is why modern best practice is to _______.",
                "answer": "445; WannaCry; SMBv1; disable SMBv1 entirely.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user can browse the internet normally but cannot connect to the company's internal\n    file server or map any network drives. You run netstat on the file server and see it listening on port 445.\n    What is the most likely cause and how do you confirm it?",
                "answer": "A firewall rule is blocking TCP port 445 between the user's subnet and the file server. Confirm by checking the firewall policy for rules affecting SMB/port 445. Test by attempting a connection with telnet or a port scanner (nmap) to the server on port 445 from the affected workstation — a timeout or connection refused confirms the block. Also check Windows Firewall on the server itself.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.5.2": {
        "unit": "1.5.2",
        "title": "Protocols",
        "n10_009": "1.5",
        "n10_008": "1.5",
        "questions": [
            {
                "num": "1",
                "question": "ICMP does not carry _______ data. It operates at Layer _______ and does not use _______. The two\n    most common uses of ICMP in troubleshooting are _______ and _______.",
                "answer": "User; Layer 3; port numbers; ping (Echo Request/Reply); traceroute/tracert (Time Exceeded messages).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "If ping fails to a host that is actually up and running, the most likely reason is _______. This means a\n    failed ping does NOT automatically mean _______.",
                "answer": "ICMP is being filtered/blocked by a firewall or security policy; the host is down.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "ARP resolves _______ addresses to _______ addresses. A device broadcasts an ARP _______ to the\n    segment, and the target responds with a unicast ARP _______. The result is stored in the device's\n    _______ table.",
                "answer": "IP; MAC; Request; Reply; ARP cache.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Write out the DHCP DORA process:\n    D — _______\n    O — _______\n    R — _______\n    A — _______",
                "answer": "D — Discover (client broadcasts looking for a DHCP server); O — Offer (server offers an IP address and config); R — Request (client formally requests the offered address); A — Acknowledge (server confirms the lease).",
                "lines": 5
            },
            {
                "num": "5",
                "question": "A rogue DHCP server occurs when _______. The symptom on affected workstations is _______. To\n    find the rogue server, you would _______.",
                "answer": "An unauthorized device (e.g., a home router plugged into the network) starts responding to DHCP Discover broadcasts; devices receive incorrect IP configurations (wrong gateway, wrong DNS) and lose connectivity; check DHCP server logs, use a packet capture to see which MAC address is sending DHCP Offers, or enable DHCP snooping on managed switches.",
                "lines": 6
            },
            {
                "num": "6",
                "question": "In the DNS resolution process, if the local DNS server doesn't have a cached answer, it queries a\n    _______ name server first, which directs it to the _______ server for the domain's extension, which\n    directs it to the _______ name server that has the actual IP address.",
                "answer": "Root; TLD (top-level domain, e.g., .com); authoritative.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Before HTTP data moves over HTTPS, the client and server perform a _______ handshake. The\n    server presents a _______ to prove its identity. All traffic after this point is _______ on port _______.",
                "answer": "TLS; certificate; encrypted; 443.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user reports 'the internet is down.' You run ping 8.8.8.8 — it succeeds. You run ping\n    google.com — it fails. Walk through your diagnosis and fix.",
                "answer": "IP connectivity is working (ping by IP succeeds), but DNS resolution is failing (ping by name fails). Diagnosis: check the workstation's configured DNS server (ipconfig /all). Try nslookup google.com — if it times out or returns a server failure, the DNS server is unreachable or not functioning. Fix options: confirm the DNS server IP is correct (not a DHCP misconfiguration), check if the DNS server is running, check firewall rules for UDP/TCP port 53 between the client and DNS server, or temporarily configure a known-good DNS server (8.8.8.8) to confirm the fix.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "1.6.1": {
        "unit": "1.6.1",
        "title": "Dhcp",
        "n10_009": "1.6",
        "n10_008": "1.6",
        "questions": [
            {
                "num": "1",
                "question": "A DHCP scope defines the _______ of addresses available for assignment, the _______ time, and\n    options such as _______, _______, and _______. Exclusions are addresses within the scope range\n    that the server will _______.",
                "answer": "Range; lease; default gateway, DNS server, domain name (any two); never assign.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A DHCP reservation assigns a _______ IP address to a specific device based on its _______. This\n    differs from a static IP because the address is still managed by _______ rather than configured\n    manually on the device.",
                "answer": "Permanent (fixed); MAC address; the DHCP server.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "When a DHCP lease is _______ % expired, the client attempts to renew with the same server. If the\n    server is unavailable when the lease fully expires, the client falls back to _______ and starts the\n    _______ process over.",
                "answer": "50%; APIPA (169.254.x.x); DORA.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A DHCP relay agent (helper address) is needed when _______. The relay agent is configured on the\n    _______ and forwards DHCP broadcasts as _______ packets to the DHCP server's IP address.",
                "answer": "The DHCP server and client are on different subnets (routers don't forward broadcasts by default); the router/Layer 3 switch interface; unicast.",
                "lines": 4
            },
            {
                "num": "5",
                "question": "DHCP failover has two modes. In _______ mode, one server handles all leases and the other takes\n    over only if the primary fails. In _______ mode, both servers share the address pool and handle\n    requests simultaneously.",
                "answer": "Hot-standby; load-balance.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Match each DHCP problem to its symptom:\n    Exhausted scope ﬁ _______\n    Rogue DHCP server ﬁ _______\n    Misconfigured relay ﬁ _______\n    IP address conflict ﬁ _______\n    Answer: Exhausted scope ﬁ new devices get APIPA addresses, existing leases still work; Rogue\n    DHCP server ﬁ devices get wrong gateway/DNS, lose connectivity; Misconfigured relay ﬁ devices on\n    remote subnets get APIPA; IP conflict ﬁ both devices show warnings, intermittent connectivity for one\n    or both.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "To check available addresses in a Windows DHCP scope, you would use _______. To force a client to\n    release and request a new lease, the commands are _______ followed by _______.",
                "answer": "DHCP Manager console (or netsh/PowerShell); ipconfig /release; ipconfig /renew.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: On Monday morning, 30 students in one classroom can't get on the network. They all\n    have 169.254.x.x addresses. Students in other classrooms are fine. Walk through your diagnosis in\n    order.",
                "answer": "1. APIPA on all devices in one segment = DHCP failure isolated to that subnet. 2. Check the DHCP scope for that subnet — is it exhausted? 3. Check the relay agent (helper address) on the switch or router interface for that VLAN — is it configured and pointing to the correct DHCP server? 4. Check if the DHCP server is running and the scope is active. 5. Check for a rogue DHCP server on that segment (packet capture or DHCP snooping logs). 6. Try ipconfig /release /renew on one workstation after each fix to confirm.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "1.6.2": {
        "unit": "1.6.2",
        "title": "Dns",
        "n10_009": "1.6",
        "n10_008": "1.6",
        "questions": [
            {
                "num": "1",
                "question": "Match each DNS record type to its purpose:\n    A ﬁ _______\n    AAAA ﬁ _______\n    CNAME ﬁ _______\n    MX ﬁ _______\n    PTR ﬁ _______",
                "answer": "A ﬁ maps hostname to IPv4 address; AAAA ﬁ maps hostname to IPv6 address; CNAME ﬁ alias pointing one hostname to another; MX ﬁ identifies mail servers for the domain; PTR ﬁ reverse lookup, maps IP address to hostname.",
                "lines": 5
            },
            {
                "num": "2",
                "question": "A TXT record stores _______ data in DNS. Common uses include _______ (proves domain ownership\n    to email providers) and _______ (specifies which servers are authorized to send email for the domain).",
                "answer": "Arbitrary text; DKIM/DMARC verification; SPF (Sender Policy Framework).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A forward lookup zone resolves _______ to _______. A reverse lookup zone resolves _______ to\n    _______. Reverse lookups are used primarily for _______ and _______.",
                "answer": "Hostnames to IP addresses; IP addresses to hostnames; logging/auditing and email spam verification (PTR checks).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "An authoritative DNS server holds the _______ records for a zone and gives definitive answers. A\n    recursive resolver queries _______ on behalf of clients, caching results for up to the record's _______\n    value.",
                "answer": "Actual/original; other DNS servers; TTL (Time to Live).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "DNS cache poisoning occurs when _______. An attacker who succeeds can redirect users to _______.\n    The defense against this attack is _______, which adds cryptographic signatures to DNS responses.",
                "answer": "An attacker inserts false DNS records into a resolver's cache; a malicious server (phishing, malware distribution); DNSSEC (DNS Security Extensions).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Split-horizon DNS serves _______ DNS responses to internal clients and _______ DNS responses to\n    external clients for the same domain name. This allows internal users to reach _______ while external\n    users reach _______.",
                "answer": "Different; different; internal servers by private IP; the same service via public IP (or a DMZ address).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The command _______ queries DNS and shows the record type, answer, and which server responded.\n    The command _______ is a more detailed alternative available on Linux/Mac. To test a specific DNS\n    server directly, the syntax is _______.",
                "answer": "nslookup; dig; nslookup hostname server-ip (or dig @server-ip hostname).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user can reach internal file servers by IP but not by name. External websites resolve\n    fine. nslookup on their workstation returns correct results for external domains but times out for internal\n    hostnames. What is the most likely cause and how do you fix it?",
                "answer": "The workstation is querying an external DNS server (e.g., 8.8.8.8) instead of the internal DNS server, which hosts the internal zone. The external server has no records for internal hostnames. Fix: check the workstation's DNS server setting (ipconfig /all) — it should point to the internal DNS server. This is often caused by a DHCP misconfiguration (wrong DNS option) or a manual static DNS setting on the workstation. Correct the DNS server assignment and test with nslookup.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.6.3": {
        "unit": "1.6.3",
        "title": "Ntp",
        "n10_009": "1.6",
        "n10_008": "1.6",
        "questions": [
            {
                "num": "1",
                "question": "List three network systems or services that break or behave incorrectly when clocks are not\n    synchronized:\n    1. _______\n    2. _______\n    3. _______",
                "answer": "Any three: Kerberos authentication (rejects tickets if clock skew exceeds 5 minutes); log correlation (events appear out of order across devices); certificate validation (wrong date causes rejection of valid certs or acceptance of expired ones); scheduled tasks/replication (fire at wrong time or collide).",
                "lines": 5
            },
            {
                "num": "2",
                "question": "Stratum 0 is the _______ itself (e.g., atomic clock or GPS). Stratum 1 servers are directly connected to\n    _______. Stratum 16 means _______.",
                "answer": "Reference clock (hardware); a Stratum 0 source; unsynchronized — the server has lost contact with its upstream source.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "In a typical enterprise network, the internal NTP server syncs to an external _______ or _______\n    source. All other network devices then sync to _______. This design limits external NTP traffic to\n    _______ connection.",
                "answer": "Stratum 1; Stratum 2; the internal NTP server; a single.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "SNTP differs from NTP in that it _______. SNTP is acceptable for _______ devices. Full NTP is\n    preferred for _______ where millisecond accuracy matters.",
                "answer": "Simply snaps the clock to the server's time without continuously adjusting for latency/drift; client devices (workstations, phones, IoT); servers, routers, and infrastructure devices.",
                "lines": 4
            },
            {
                "num": "5",
                "question": "NTP uses port _______ / protocol _______. Best practice is to configure at least _______ NTP sources\n    so that clients can _______ responses and detect a bad time source.",
                "answer": "UDP port 123; at least two; compare/validate.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "In a Windows Active Directory environment, workstations sync time to their _______. Domain\n    controllers sync to the _______. The PDC emulator should be configured to sync to _______. If this last\n    step is skipped, the result is _______.",
                "answer": "Authenticating domain controller; PDC emulator; an external NTP source; the entire domain's time drifts, eventually causing Kerberos authentication failures.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A device reports Stratum 16. This means _______. To troubleshoot, you would _______.",
                "answer": "The device is unsynchronized — it has lost contact with its upstream NTP source. Trace the NTP chain upstream: check if the configured NTP server is reachable (ping/UDP 123), check firewall rules for UDP 123, verify the upstream server itself is synchronized.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: Monday morning, no staff can log in to their Windows workstations. Error messages\n    say 'authentication failure' but credentials are correct. What is the first thing you check and why?",
                "answer": "Check the time on the domain controller and compare it to an accurate external reference (e.g., time.google.com or the system clock on a phone). Kerberos authentication fails if client and DC clocks differ by more than 5 minutes. A drifted DC clock matches this exact symptom — all logins fail simultaneously with vague auth errors. Fix by correcting the DC clock and verifying NTP is configured and running.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.7.1": {
        "unit": "1.7.1",
        "title": "Corporate Datacenter Architecture",
        "n10_009": "1.7",
        "n10_008": "1.7",
        "questions": [
            {
                "num": "1",
                "question": "In three-tier architecture, match each layer to its primary function:\n    Access layer ﬁ _______\n    Distribution layer ﬁ _______\n    Core layer ﬁ _______",
                "answer": "Access ﬁ end devices connect here; provides port density, PoE, VLAN assignment; Distribution ﬁ aggregates access switches, handles inter-VLAN routing, applies ACLs and policies; Core ﬁ backbone, moves traffic between distribution blocks at wire speed with no filtering.",
                "lines": 5
            },
            {
                "num": "2",
                "question": "A collapsed core design merges the _______ and _______ layers into one. It is appropriate for\n    _______ environments. It becomes a problem when _______.",
                "answer": "Distribution and core; smaller single-building; the network grows large enough that combined switches become a bottleneck or unworkable single point of failure.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "In spine-leaf architecture, every _______ switch connects to every _______ switch. No _______\n    connects directly to another _______. Any server can reach any other server in exactly _______ hops.",
                "answer": "Leaf; spine; leaf; leaf; two.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Spine-leaf exists because data centers have predominantly _______ traffic (server-to-server), while\n    three-tier was designed for _______ traffic (client-to-server). Three-tier forces server-to-server traffic\n    through _______ extra hops.",
                "answer": "East-west; north-south; multiple (up to distribution, across, back down).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "In top-of-rack switching, a switch sits _______ and servers connect with _______ cables. In end-of-row\n    switching, a larger switch serves _______ with longer cable runs. The dominant modern approach is\n    _______ because _______.",
                "answer": "At the top of each rack; short (1-3 meter); multiple racks in a row; top-of-rack; short cable runs are easier to manage and it aligns naturally with spine-leaf (each ToR = a leaf).",
                "lines": 5
            },
            {
                "num": "6",
                "question": "SDN separates the _______ plane (forwarding decisions) from the _______ plane (actual packet\n    forwarding). A centralized _______ pushes decisions to network devices, which become simple\n    _______.",
                "answer": "Control; data; SDN controller; forwarding engines.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "NFV replaces dedicated hardware _______ with software running on _______. The key advantages\n    are _______ and _______. Examples of virtualized network functions include _______.",
                "answer": "Appliances (firewalls, load balancers, IDS/IPS); standard server hardware (hypervisors/containers); flexibility and reduced cost; virtual firewalls, virtual load balancers, virtual WAN optimizers (any two).",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: You're told the data center is experiencing high latency between application servers\n    that frequently communicate. The current design is three-tier. What architecture change would you\n    recommend and why?",
                "answer": "Recommend migrating to spine-leaf architecture. The problem is east-west traffic (server-to-server) being forced through multiple hops in three-tier — up to distribution, across to another distribution switch, back down. Spine-leaf reduces this to exactly two hops (up to spine, down to destination leaf) with consistent, predictable latency. Add leaf switches for server density and spine switches for bandwidth as needed without redesigning the whole network.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.7.2": {
        "unit": "1.7.2",
        "title": "Cloud Concepts",
        "n10_009": "1.7",
        "n10_008": "1.7",
        "questions": [
            {
                "num": "1",
                "question": "Match each cloud service model to what the customer is responsible for managing:\n    IaaS ﬁ _______\n    PaaS ﬁ _______\n    SaaS ﬁ _______",
                "answer": "IaaS ﬁ OS, applications, data, access controls (everything from OS up); PaaS ﬁ application code and data; SaaS ﬁ access management (accounts, permissions, MFA) and data classification.",
                "lines": 4
            },
            {
                "num": "2",
                "question": "Give one real-world example of each service model:\n    IaaS ﬁ _______\n    PaaS ﬁ _______\n    SaaS ﬁ _______",
                "answer": "IaaS ﬁ AWS EC2, Azure Virtual Machines, Google Compute Engine; PaaS ﬁ Azure App Service, AWS Elastic Beanstalk, Google App Engine; SaaS ﬁ Microsoft 365, Google Workspace, Salesforce, Zoom (any valid example).",
                "lines": 5
            },
            {
                "num": "3",
                "question": "A _______ cloud is shared infrastructure available to any paying customer. A _______ cloud is\n    dedicated to a single organization. A _______ cloud combines both. A _______ cloud is shared among\n    organizations with common requirements (e.g., government agencies).",
                "answer": "Public; private; hybrid; community.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A dedicated cloud connection (AWS calls it _______, Azure calls it _______) differs from a VPN\n    connection because it _______. The tradeoff is _______.",
                "answer": "Direct Connect; ExpressRoute; bypasses the public internet entirely, providing consistent bandwidth and predictable latency; significantly higher cost.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "In cloud networking, a _______ (VPC/VNet) is an isolated network environment. Within it, _______\n    divide the address space by purpose. _______ act as virtual firewalls attached to resources, controlling\n    inbound and outbound traffic with stateful rules.",
                "answer": "Virtual network; subnets; security groups.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The shared responsibility model means that in IaaS, if an attacker exploits an unpatched OS\n    vulnerability on a cloud VM, the responsibility belongs to _______. The cloud provider is responsible for\n    _______.",
                "answer": "The customer (they manage the OS and patching); the physical infrastructure, hypervisor, and network fabric.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A cloud load balancer sits in front of multiple backend instances and provides: (1) _______, (2)\n    _______, and (3) _______. It keeps the application available when individual instances _______.",
                "answer": "Traffic distribution across healthy instances; health checks (routes away from failed instances); SSL/TLS termination; fail.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A teacher reports that Microsoft 365 is slow during first period but fast after 9 AM. The\n    internet connection looks fine from the server room. What cloud-specific factors would you investigate?",
                "answer": "1. Check bandwidth utilization on the internet uplink during first period — 30+ students authenticating and syncing OneDrive simultaneously can saturate an undersized connection. 2. Check QoS policies — is Microsoft 365 traffic prioritized over general browsing? 3. Review DNS resolution time for M365 endpoints — slow DNS adds latency at connection establishment. 4. Check if the district uses a web proxy or content filter that may be bottlenecking M365 traffic. 5. Consider split tunneling if traffic routes through a VPN. Microsoft publishes recommended network configurations for M365 that include direct internet breakout for their endpoints.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "1.8.1": {
        "unit": "1.8.1",
        "title": "Routing Concepts",
        "n10_009": "1.8",
        "n10_008": "1.8",
        "questions": [
            {
                "num": "1",
                "question": "A router makes forwarding decisions by consulting its _______. Each entry contains the _______\n    network, the _______ IP or exit interface, and metadata including _______ and _______. If no match\n    exists and there is no default route, the router _______.",
                "answer": "Routing table; destination; next-hop; administrative distance and metric; drops the packet and sends ICMP destination unreachable.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A routing table has entries for 10.0.0.0/8, 10.1.0.0/16, and 10.1.1.0/24. A packet destined for 10.1.1.75\n    will match _______ entries but be forwarded using the _______ route because of the _______ rule.",
                "answer": "All three; 10.1.1.0/24 (/24); longest prefix match (most specific route wins).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Connected routes appear automatically when _______. They require no manual configuration and have\n    an administrative distance of _______. A static route has an AD of _______, meaning it is trusted\n    _______ than a connected route.",
                "answer": "An IP address is assigned to a router interface and the interface comes up; 0; 1; less (higher AD = less trusted).",
                "lines": 4
            },
            {
                "num": "4",
                "question": "Static routing is appropriate for _______ networks because it is _______. It fails to scale because\n    _______. Dynamic routing solves this by _______.",
                "answer": "Small, stable; simple and predictable with no routing protocol overhead; every route must be manually configured and updated when topology changes; using protocols (OSPF, EIGRP, BGP) that let routers discover and share network information automatically.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "A default route uses the CIDR notation _______. It matches _______ destinations not covered by a\n    more specific route. Home routers use a default route pointing to _______ so they don't need to know\n    every route on the internet.",
                "answer": "0.0.0.0/0; all; the ISP's gateway.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Fill in the default administrative distance values:\n    Connected route ﬁ _______\n    Static route ﬁ _______\n    OSPF ﬁ _______\n    EIGRP ﬁ _______\n    RIP ﬁ _______",
                "answer": "Connected: 0; Static: 1; OSPF: 110; EIGRP: 90; RIP: 120.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "OSPF uses _______ as its metric, derived from _______. RIP uses _______ as its metric with a\n    maximum of _______ hops. RIP is considered inferior because _______.",
                "answer": "Cost; interface bandwidth (faster links = lower cost); hop count; 15; hop count ignores link speed — a path with fewer hops over slow links can win over a faster path with one extra hop.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user reports they can reach some servers on the 10.2.x.x network but not others.\n    You run 'show ip route' on the edge router and see a static route for 10.2.1.0/24 and an OSPF route for\n    10.2.0.0/16. A packet to 10.2.1.50 goes where, and why? A packet to 10.2.5.50 goes where, and why?",
                "answer": "10.2.1.50 ﬁ uses the static route 10.2.1.0/24 because it is more specific (longest prefix match) and also has lower AD (1 vs 110). 10.2.5.50 ﬁ uses the OSPF route 10.2.0.0/16 because the static route does not cover that address — only the /16 matches. If the static route's next hop is unreachable, 10.2.1.x hosts would be unreachable while 10.2.5.x hosts are fine, which matches the reported symptom of 'some servers reachable, others not.'",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.8.2": {
        "unit": "1.8.2",
        "title": "Routing Protocols",
        "n10_009": "1.8",
        "n10_008": "1.8",
        "questions": [
            {
                "num": "1",
                "question": "Distance vector protocols share _______ with directly connected neighbors at regular intervals.\n    Routers only know _______ and _______ to each destination — not the full topology. Link state\n    protocols share _______ with all routers in the area, so every router builds _______.",
                "answer": "Their entire routing table; direction and distance (hop count or metric); Link State Advertisements (LSAs); an identical map of the full network topology.",
                "lines": 4
            },
            {
                "num": "2",
                "question": "RIP uses _______ as its only metric. Its maximum is _______ hops — a destination _______ hops\n    away is considered unreachable. RIP sends full table updates every _______ seconds, which causes\n    slow _______.",
                "answer": "Hop count; 15; 16; 30; convergence.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "OSPF uses _______ as its metric, derived from _______. This means OSPF prefers _______ links\n    over _______ links, unlike RIP which only counts _______.",
                "answer": "Cost; interface bandwidth; faster (higher bandwidth); slower; hops.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "In OSPF, _______ is the backbone area that all other areas must connect to. Using areas limits the\n    scope of _______ flooding and _______ calculations, allowing OSPF to scale to large networks.",
                "answer": "Area 0; LSA; SPF (Shortest Path First).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "On an Ethernet segment with multiple OSPF routers, a _______ (DR) and _______ (BDR) are elected.\n    All other routers form adjacencies only with these two. This reduces the number of _______\n    relationships from exponential to manageable.",
                "answer": "Designated Router; Backup Designated Router; adjacency/neighbor.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "EIGRP's DUAL algorithm maintains a _______ — a pre-calculated backup route. If the primary route\n    fails and one exists, EIGRP installs it _______ with no recalculation. EIGRP only sends updates when\n    _______, making it bandwidth-efficient.",
                "answer": "Feasible successor; immediately (sub-second); something changes (triggered updates).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "BGP is classified as a _______ protocol. It routes between _______ (ASes), each identified by an\n    _______. _______ BGP runs between different ASes (e.g., your router to your ISP). _______ BGP\n    runs within the same AS.",
                "answer": "Path vector; Autonomous Systems; AS number; eBGP (external); iBGP (internal).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: You inherit a network with three sites running RIP. Users at Site C (which is 14 hops\n    from Site A) report they can reach Site A fine, but a new Site D has been added 2 hops beyond Site C.\n    Users at Site D cannot reach Site A at all. Explain why and what you would do.",
                "answer": "Site D is 16 hops from Site A (14 + 2), which exceeds RIP's maximum of 15 hops. RIP treats the destination as unreachable and does not install the route. Fix: replace RIP with OSPF or EIGRP, which have no practical hop count limit. OSPF uses cost (bandwidth-based) and scales to any size network. This is also an opportunity to review whether the network design can be optimized to reduce hop count.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "1.8.3": {
        "unit": "1.8.3",
        "title": "Wan Technologies",
        "n10_009": "1.8",
        "n10_008": "1.8",
        "questions": [
            {
                "num": "1",
                "question": "Circuit switching establishes a _______ path for the duration of communication, guaranteeing _______\n    but wasting capacity when idle. Packet switching breaks data into _______ that share carrier\n    infrastructure, which is more _______ but provides no dedicated bandwidth.",
                "answer": "Dedicated; bandwidth/performance; packets; efficient.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A T1 leased line provides _______ Mbps. A T3 provides _______ Mbps. Leased lines offer _______\n    bandwidth and _______ performance. Their main disadvantage compared to modern alternatives is\n    _______.",
                "answer": "1.544 Mbps; 44.736 Mbps; guaranteed/dedicated; predictable; high cost per megabit.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "MPLS routes traffic using _______ instead of IP addresses, creating virtual circuits. It supports\n    _______ (two sites) and _______ (all sites can communicate directly) configurations. Its main\n    advantage over broadband is _______ for latency, jitter, and packet loss.",
                "answer": "Labels; point-to-point; any-to-any (full mesh); SLA guarantees.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Metro Ethernet extends _______ connectivity beyond a single building using carrier _______. From the\n    router's perspective it looks like _______. It is typically limited to _______ geographic areas.",
                "answer": "Ethernet; metropolitan fiber network; a very long Ethernet cable (same frame format, same interface); metro/city-wide.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Match each broadband type to its key characteristic:\n    Cable ﬁ _______\n    DSL ﬁ _______\n    Fiber ﬁ _______",
                "answer": "Cable ﬁ shared neighborhood bandwidth, speeds vary at peak hours, asymmetric; DSL ﬁ runs over telephone copper, speed degrades with distance from CO, declining technology; Fiber ﬁ dedicated to premises, symmetrical speeds up to 1+ Gbps, best performance.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "An SD-WAN appliance at a branch office monitors _______, _______, and _______ on all WAN links in\n    real time. Application-aware policies send _______ traffic over the highest-quality link and _______\n    traffic over cheaper broadband.\n    Answer: Latency; jitter; packet loss (bandwidth); voice/video (latency-sensitive); web browsing/cloud\n    application.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "The 'last mile' refers to _______. It is often the _______ in WAN performance. Installing fiber last mile\n    to a building that doesn't have it can take _______, which affects WAN planning timelines.",
                "answer": "The connection between the carrier's network infrastructure and the customer's building; bottleneck; weeks to months.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: Your organization has 20 branch offices each paying $1,800/month for MPLS. A\n    vendor proposes replacing each with $150/month fiber broadband plus an SD-WAN appliance. What\n    questions do you ask before approving the change?",
                "answer": "1. Is fiber available at all 20 locations (last mile)? 2. What are the SLA terms on the fiber broadband vs current MPLS? 3. Which applications are latency/jitter sensitive (voice, video, real-time systems) — will SD-WAN's dynamic path selection meet their requirements? 4. What is the SD-WAN licensing and appliance cost — calculate true TCO not just circuit savings? 5. What is the failover/redundancy plan if the single broadband link goes down (LTE backup)? 6. Does the SD-WAN solution support existing security policies and integrations?",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "2.1.1": {
        "unit": "2.1.1",
        "title": "Switching Concepts",
        "n10_009": "2.1",
        "n10_008": "2.1",
        "questions": [
            {
                "num": "1",
                "question": "A switch learns MAC addresses by reading the _______ on every incoming frame and recording which\n    _______ it arrived on. Entries age out after typically _______ seconds. This table is also called the\n    _______ table.",
                "answer": "Source MAC address; port; 300 seconds; CAM (Content Addressable Memory).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Match each switching behavior to its condition:\n    Forwarding ﬁ _______\n    Filtering ﬁ _______\n    Flooding ﬁ _______",
                "answer": "Forwarding ﬁ destination MAC is in the table on a different port, send out that port only; Filtering ﬁ destination MAC is on the same port the frame arrived on, drop it; Flooding ﬁ destination MAC is unknown or it's a broadcast, send out all ports except the source port.",
                "lines": 5
            },
            {
                "num": "3",
                "question": "Each switch port is its own _______ domain, eliminating collisions. By default, the entire switch is one\n    _______ domain — a broadcast reaches every port. _______ and _______ are the two tools used to\n    break broadcast domains.",
                "answer": "Collision; broadcast; Routers; VLANs.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Full duplex allows a device to _______ and _______ simultaneously, effectively doubling available\n    bandwidth. A duplex mismatch occurs when one side negotiates _______ and the other negotiates\n    _______. The symptom is _______.",
                "answer": "Transmit; receive; full duplex; half duplex; high latency, excessive errors, late collisions — connection works but performs very poorly.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Without STP, redundant switch links create _______. A broadcast frame enters the loop and circulates\n    _______, multiplying at every junction. This is called a _______ and will take down the network in\n    seconds.",
                "answer": "Layer 2 loops; forever; broadcast storm.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "In STP, the switch with the lowest _______ becomes the root bridge. The Bridge ID is composed of\n    _______ and _______. In production, you should set _______ manually to control which switch wins\n    the election.",
                "answer": "Bridge ID; priority value; MAC address; priority.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A port in STP _______ state receives BPDUs but does not forward frames. The transition from blocking\n    to forwarding in classic STP takes approximately _______ seconds. RSTP reduces this to _______\n    and consolidates port states to: _______, _______, and _______.",
                "answer": "Blocking; 30-50; seconds (sub-second to a few seconds); Discarding, Learning, Forwarding.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user plugs a cheap unmanaged switch into a wall jack to add more ports at their\n    desk. Within seconds, the entire floor loses network connectivity. Explain what happened and what\n    configuration would have prevented it.",
                "answer": "The unmanaged switch created a Layer 2 loop — its ports connected back to the network in multiple places with no STP awareness, causing a broadcast storm. Prevention: enable PortFast on all access ports (so end devices come up immediately) combined with BPDU Guard (which shuts down the port the instant it receives a BPDU from a connected switch). BPDU Guard would have shut down the port when the unmanaged switch sent a BPDU, containing the damage immediately.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "2.1.2": {
        "unit": "2.1.2",
        "title": "Vlans",
        "n10_009": "2.1",
        "n10_008": "2.1",
        "questions": [
            {
                "num": "1",
                "question": "A VLAN creates a separate _______ domain on a switch. Devices on different VLANs cannot\n    communicate at Layer 2 even if they are plugged into the _______. VLAN IDs range from _______ to\n    _______. Best practice is to avoid using VLAN _______ for production traffic.",
                "answer": "Broadcast; same physical switch; 1; 4094; VLAN 1.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "An access port belongs to _______ VLAN and connects to _______. A trunk port carries traffic for\n    _______ VLANs simultaneously and typically connects _______.",
                "answer": "One; end devices (workstations, printers, cameras); multiple; switches to switches or switches to routers.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "802.1Q tagging inserts a _______ -byte tag into the Ethernet frame on trunk links. The tag contains the\n    _______. When a frame exits an _______ port to an end device, the tag is _______.",
                "answer": "4-byte; VLAN ID; access; removed/stripped.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "The native VLAN is sent across a trunk _______. If the native VLAN doesn't match on both ends of a\n    trunk, frames end up _______. Best practice is to change the native VLAN away from _______ and\n    ensure it _______ on both sides.",
                "answer": "Untagged (no 802.1Q tag); in the wrong VLAN (traffic leak/mismatch); VLAN 1; matches.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Router-on-a-stick uses _______ on a single router interface — one per VLAN — each configured with\n    the _______ IP for that VLAN. Its limitation is _______. Layer 3 switching uses _______ (SVIs) on the\n    switch itself and routes at _______.",
                "answer": "Subinterfaces; gateway; all inter-VLAN traffic funnels through one physical interface (bottleneck); Switched Virtual Interfaces; wire speed in hardware.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A voice VLAN allows one physical port to carry both _______ traffic (untagged, data VLAN) and\n    _______ traffic (tagged, voice VLAN). The IP phone negotiates its VLAN via _______ or _______. QoS\n    policies on the voice VLAN ensure _______.",
                "answer": "PC/data; voice; CDP; LLDP; voice packets are prioritized for call quality.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Match each VLAN misconfiguration to its symptom:\n    Wrong VLAN assignment ﬁ _______\n    Trunk not formed ﬁ _______\n    VLAN not allowed on trunk ﬁ _______\n    No inter-VLAN routing ﬁ _______",
                "answer": "Wrong VLAN ﬁ device gets wrong DHCP address or none, can't reach resources; Trunk not formed ﬁ VLANs don't extend between switches; VLAN not allowed ﬁ traffic for that specific VLAN won't cross the trunk; No routing ﬁ devices on different VLANs can't communicate even with correct addresses.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A new teacher's workstation is connected but can only reach devices in the front office,\n    not classroom resources. Other teachers on the same switch can reach everything. What do you check\n    first and why?",
                "answer": "Check the VLAN assignment on that specific switch port with 'show vlan brief' or 'show interfaces switchport'. The port is likely assigned to the administration VLAN (front office) instead of the staff/classroom VLAN. Verify what IP address the workstation received — if it's in the admin subnet, that confirms the wrong VLAN. Correct the access VLAN assignment on the port and have the workstation renew its DHCP lease.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "2.1.3": {
        "unit": "2.1.3",
        "title": "Switch Configuration",
        "n10_009": "2.1",
        "n10_008": "2.1",
        "questions": [
            {
                "num": "1",
                "question": "The first access method used on a new unconfigured switch is a _______ cable connected to the\n    _______ port. Terminal settings are: _______ baud, _______ data bits, _______ parity, _______ stop\n    bit.",
                "answer": "Console (rollover); console port; 9600 baud; 8 data bits; no parity; 1 stop bit.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "You should always use _______ instead of _______ to protect the privileged EXEC password, because\n    the latter stores it in _______. The command _______ applies weak encryption to all plaintext\n    passwords in the config.",
                "answer": "enable secret; enable password; plaintext; service password-encryption.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "To configure SSH, three prerequisites are required: (1) _______, (2) _______, and (3) _______. The\n    VTY lines must be set to _______ to prevent Telnet access.",
                "answer": "Hostname configured; IP domain name configured; RSA key pair generated (crypto key generate rsa); transport input ssh.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Write the commands to create VLAN 10 named CLASSROOM and assign GigabitEthernet0/1 to it as\n    an access port:\n    _______\n    _______\n    _______\n    _______\n    _______",
                "answer": "vlan 10 / name CLASSROOM / exit / interface GigabitEthernet0/1 / switchport mode access / switchport access vlan 10",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Write the commands to configure GigabitEthernet0/48 as a trunk carrying VLANs 10, 20, and 30 with\n    native VLAN 99:\n    _______\n    _______\n    _______",
                "answer": "interface GigabitEthernet0/48 / switchport mode trunk / switchport trunk allowed vlan 10,20,30 / switchport trunk native vlan 99",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The running-config lives in _______ and is lost on reboot. The startup-config is loaded at boot. The\n    command to save is _______. If you skip this step after making changes and the switch reboots, the\n    result is _______.",
                "answer": "RAM; copy running-config startup-config (or copy run start); all configuration changes are lost.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Match each show command to what it verifies:\n    show vlan brief ﬁ _______\n    show interfaces trunk ﬁ _______\n    show mac address-table ﬁ _______\n    show interfaces Gi0/1 ﬁ _______",
                "answer": "show vlan brief ﬁ VLAN assignments per port; show interfaces trunk ﬁ active trunks, allowed VLANs, native VLAN; show mac address-table ﬁ learned MAC addresses and which port each is on; show interfaces Gi0/1 ﬁ speed, duplex, error counters, status.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: After configuring VLANs and trunks on two switches, devices on VLAN 20 can't\n    communicate between switches but VLAN 10 works fine. What commands do you run and what are\n    you looking for?",
                "answer": "Run 'show interfaces trunk' on both switches. Check: (1) Is the trunk port in trunking mode on both sides? (2) Is VLAN 20 in the allowed VLAN list on both sides? (3) Does the native VLAN match? Run 'show vlan brief' to confirm VLAN 20 exists on both switches — a VLAN must be created locally on each switch to be active. The most likely cause is VLAN 20 not being in the allowed list on the trunk, or VLAN 20 not existing on one of the switches.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "2.2.1": {
        "unit": "2.2.1",
        "title": "Wireless Standards",
        "n10_009": "2.2",
        "n10_008": "2.2",
        "questions": [
            {
                "num": "1",
                "question": "The 2.4 GHz band offers better _______ and _______ than 5 GHz but has only _______\n    non-overlapping channels in the US and suffers from more _______ from non-Wi-Fi devices.",
                "answer": "Range; wall penetration; three (channels 1, 6, 11); interference.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "The 6 GHz band, used by Wi-Fi _______ and Wi-Fi _______, provides approximately _______ MHz of\n    spectrum. Its main limitation compared to 5 GHz is _______ and _______.",
                "answer": "Wi-Fi 6E; Wi-Fi 7; 1200 MHz; shorter range; worse wall penetration.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Fill in the theoretical maximum throughput for each standard:\n    802.11b ﬁ _______\n    802.11a ﬁ _______\n    802.11g ﬁ _______\n    802.11n ﬁ _______\n    802.11ac ﬁ _______\n    802.11ax ﬁ _______",
                "answer": "b: 11 Mbps; a: 54 Mbps; g: 54 Mbps; n: 600 Mbps; ac: 6.93 Gbps; ax: 9.6 Gbps.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "MIMO uses multiple _______ to send parallel _______ over the same channel. A '4x4' device has\n    _______ transmit and _______ receive antennas. If a 4x4 AP talks to a 2x2 client, the client gets\n    _______ streams.",
                "answer": "Antennas; spatial streams; 4; 4; two streams (limited by the client).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "MU-MIMO allows the AP to communicate with _______ clients simultaneously. Wi-Fi 5 added\n    MU-MIMO on the _______. Wi-Fi 6 added MU-MIMO on the _______ as well.",
                "answer": "Multiple; downlink (AP to clients); uplink (clients to AP).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Wi-Fi 6 introduced _______ which lets the AP divide a channel into sub-channels to serve multiple\n    clients per transmission. _______ reduces interference by tagging frames so devices ignore signals\n    from neighboring networks on the same channel.",
                "answer": "OFDMA (Orthogonal Frequency Division Multiple Access); BSS Coloring.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "In a high-density environment, wider channels provide _______ per client but leave _______\n    non-overlapping channels. Best practice for dense deployments is _______ channels with _______ AP\n    density.",
                "answer": "More throughput; fewer; narrower; higher.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school deploys Wi-Fi 6 APs in every classroom. During standardized testing, 30\n    Chromebooks per room are all active simultaneously and performance is poor. What Wi-Fi 6 features\n    specifically address this scenario, and what configuration changes would you make?",
                "answer": "OFDMA addresses high-density small-packet traffic by serving multiple clients per transmission instead of taking turns. MU-MIMO (uplink and downlink) allows simultaneous transmissions. BSS Coloring reduces co-channel interference from adjacent classroom APs. Configuration: ensure 5 GHz with 20 MHz channels (maximizes non-overlapping channels), verify AP placement gives sufficient coverage without excessive overlap, enable band steering to push capable devices to 5 GHz, and confirm OFDMA and MU-MIMO are enabled in the AP configuration.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "2.2.2": {
        "unit": "2.2.2",
        "title": "Wireless Security",
        "n10_009": "2.2",
        "n10_008": "2.2",
        "questions": [
            {
                "num": "1",
                "question": "WEP is broken because its _______ -bit initialization vector space is too small, causing IVs to _______.\n    This allows an attacker to crack the key in under _______. WEP should _______ be deployed.",
                "answer": "24-bit; repeat after enough traffic is captured; a minute (with freely available tools); never.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "WPA used _______ as its encryption protocol, which wrapped around the same _______ cipher as\n    WEP. WPA2 replaced this with _______, which uses the _______ block cipher with 128-bit keys.",
                "answer": "TKIP (Temporal Key Integrity Protocol); RC4; AES-CCMP; AES (Advanced Encryption Standard).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "WPA3 replaces the PSK handshake with _______ (SAE), which makes offline brute-force attacks\n    _______ because the attacker must _______ for each guess. WPA3 also provides _______, meaning\n    captured traffic cannot be decrypted even if the password is later compromised.",
                "answer": "Simultaneous Authentication of Equals; impossible/impractical; interact with the AP; forward secrecy.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "WPA2/WPA3 Personal uses a _______ shared by all users. Enterprise uses _______ where each user\n    authenticates with _______ credentials. The AP passes authentication to a _______ server which\n    checks against a directory.",
                "answer": "Single pre-shared password; 802.1X; unique individual; RADIUS.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Enterprise mode advantages over Personal include: (1) _______, (2) _______, (3) _______, and (4)\n    _______.",
                "answer": "Individual user accountability; dynamic VLAN assignment per user; per-user encryption keys; centralized revocation (disable account = immediate removal from network).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "On 2.4 GHz, the only three non-overlapping channels are _______, _______, and _______. Using\n    channel 3 causes _______ interference which is _______ than using the same channel as a neighbor\n    because devices can't decode the signal cleanly but still wait for it.",
                "answer": "1; 6; 11; adjacent channel (ACI); worse.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A rogue AP is _______ connected to your network without authorization. An evil twin is _______ that\n    mimics a legitimate network. Evil twin attacks are more dangerous against _______ mode networks\n    because clients have no way to verify the AP's _______.",
                "answer": "Any access point; a deliberate attacker-controlled AP; Personal (PSK); identity/certificate.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A teacher reports that their laptop keeps connecting to a network called 'STAFF' but\n    then has no internet access and gets strange certificate warnings. Other staff are unaffected. What\n    attack is likely occurring and what steps do you take?",
                "answer": "This is likely an evil twin attack — an attacker has set up a rogue AP with the SSID 'STAFF' and a stronger signal than the legitimate AP. The certificate warning indicates the rogue AP's TLS certificate doesn't match the legitimate RADIUS server's certificate. Steps: (1) Check wireless controller for unknown BSSIDs broadcasting 'STAFF'. (2) Use a wireless analyzer to locate the rogue AP by signal strength. (3) Remove or disable the rogue device. (4) Verify the teacher's device is configured to validate the RADIUS server certificate and reject unknown certificates. (5) Ensure WPA3 transition mode is enabled — SAE makes this attack harder.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "3.1.1": {
        "unit": "3.1.1",
        "title": "Network Documentation",
        "n10_009": "3.1",
        "n10_008": "3.1",
        "questions": [
            {
                "num": "1",
                "question": "A _______ diagram shows the logical layout of a network — IP address ranges, VLANs, routing paths,\n    and subnets — without regard to physical location. A _______ diagram shows where devices actually\n    sit — buildings, racks, cable runs, and port connections.",
                "answer": "Logical diagram; physical diagram.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "What is IPAM, and why is it more reliable than a spreadsheet for tracking IP address assignments on a\n    large network?",
                "answer": "IPAM (IP Address Management) is a dedicated system that tracks IP address allocations, DHCP scopes, and DNS records in one place. Unlike a spreadsheet, IPAM enforces uniqueness, flags conflicts, integrates with DHCP and DNS servers, and provides search and audit capabilities. Spreadsheets go stale and create conflicts; IPAM stays authoritative.",
                "lines": 5
            },
            {
                "num": "3",
                "question": "A VLAN table documents each VLAN's _______, _______, and the _______ it connects to. Without\n    this table, adding a new switch to the network means guessing which VLANs to configure.",
                "answer": "VLAN ID, name/purpose, and the subnets (or SVIs/default gateways) it connects to.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A network baseline captures normal metrics — bandwidth utilization, CPU load, latency — during\n    _______ operation. Explain how a baseline helps during troubleshooting.",
                "answer": "Normal (steady-state) operation. A baseline gives you a reference point — if current latency is 40ms and the baseline is 2ms, something is wrong. Without a baseline, you can't distinguish abnormal from normal. It turns 'this feels slow' into 'this is 20x above normal.'",
                "lines": 5
            },
            {
                "num": "5",
                "question": "Rack documentation should include each device's _______, its _______ connections (what's plugged\n    into which port), and the device's _______. Why does this matter when a device needs to be replaced\n    at 3 AM?",
                "answer": "Rack unit (RU) position; cable/port connections; management IP (and console access method). At 3 AM, you need to know where the device is, how to access it, and what it connects to — without turning every cable over to read labels or checking a colleague's memory.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "The _______ log records every configuration change made to the network — what changed, when,\n    who made it, and why. How does this directly speed up troubleshooting?\n    Answer: Change log. When something breaks, the first question is 'what changed?' A change log\n    answers that in seconds. Without it, troubleshooting starts with hypothesis and elimination instead of a\n    known starting point.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Standard Operating Procedures (SOPs) document how to perform _______ tasks. Explain why\n    'knowledge in people's heads' is a liability, and what happens when those people are unavailable.",
                "answer": "Routine/repeatable tasks. Undocumented knowledge creates a single point of failure in the team. When the person who knows the process is on vacation, sick, or leaves the organization, that knowledge walks out with them. SOPs make processes reproducible regardless of who performs them.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: You inherit a network with no documentation. Describe the order in which you would\n    build documentation from scratch, and explain why you would start with that first item.",
                "answer": "Start with a physical diagram and device inventory — you need to know what exists and where before you can document anything else. Then: logical diagram (Layer 3 topology, subnets), VLAN table, IP address inventory (IPAM or spreadsheet), cable labels, then SOPs. The physical inventory comes first because everything else builds on knowing what devices are present.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "3.1.2": {
        "unit": "3.1.2",
        "title": "Network Monitoring",
        "n10_009": "3.1",
        "n10_008": "3.1",
        "questions": [
            {
                "num": "1",
                "question": "SNMP (Simple Network Management Protocol) uses a _______ model where the monitoring server\n    polls devices, and a _______ model where devices send unsolicited alerts when a threshold is crossed.\n    The alert message is called a _______.",
                "answer": "Poll/pull; trap (push); trap (SNMP trap).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "SNMPv1 and v2c transmit community strings in _______. SNMPv3 adds _______ and _______. Which\n    version should be used on any production network and why?",
                "answer": "Cleartext (plaintext); authentication; encryption. SNMPv3 — sending community strings in cleartext exposes management credentials to anyone capturing traffic on the network.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "NetFlow exports _______ data from routers and switches — source/destination IP, port, protocol, byte\n    count, and timestamps — without capturing the actual payload. Name two security use cases for\n    NetFlow data.",
                "answer": "Traffic flow (metadata); detecting port scans (one host hitting many ports in rapid succession), identifying data exfiltration (large unexpected outbound transfers), spotting C2 traffic patterns, finding rogue DHCP servers.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "Syslog collects log messages from network devices to a central _______ server. Severity levels range\n    from _______ (most critical, level 0) to _______ (least critical, level 7). Why is centralized logging more\n    valuable than reading logs on each device individually?",
                "answer": "Syslog; Emergency; Debug. Centralized logs allow correlation across devices — an attack that touches five switches appears as a pattern in one place rather than as isolated events on five separate devices.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "Interface utilization monitoring tracks the percentage of available bandwidth in use on each link. A link\n    consistently running above _______ % utilization is considered congested and a candidate for upgrade\n    or load balancing. What user symptom typically accompanies sustained high utilization?",
                "answer": "70–80% (accept any reasonable threshold, typically 70-80%); slow file transfers, buffering video, high latency, dropped VoIP calls.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A network monitoring system uses _______ to determine if a device is reachable. If a device stops\n    responding, the system generates an _______ to notify the administrator. What is the risk of alert\n    fatigue in a monitoring system?",
                "answer": "ICMP ping (or SNMP polling); alert/alarm. Alert fatigue occurs when too many low-priority alerts are generated — administrators begin ignoring or dismissing alerts automatically, causing real critical events to be missed.",
                "lines": 5
            },
            {
                "num": "7",
                "question": "Port mirroring (SPAN) copies traffic from one or more _______ to a designated _______ port\n    connected to a monitoring device like Wireshark or an IDS sensor. What is the limitation of using a\n    SPAN port for IDS compared to an inline IPS?",
                "answer": "Source ports (or VLANs); destination (monitor). A SPAN-connected IDS can only detect and alert — it receives a copy of the traffic and cannot block anything because it is not in the data path.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school's internet link was saturated every day from 2–3 PM for three weeks before\n    anyone noticed. No monitoring was in place. Describe a monitoring setup using two tools from this\n    lesson that would have detected this within the first day, and what each tool would have shown.",
                "answer": "1. Interface utilization monitoring (SNMP polling the uplink interface) — would have shown the uplink hitting 95-100% utilization at 2 PM daily, triggering a threshold alert immediately. 2. NetFlow analysis — would have identified which internal IPs and which protocols (likely video streaming or large file transfers) were consuming the bandwidth, enabling a targeted fix.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "3.2.1": {
        "unit": "3.2.1",
        "title": "High Availability",
        "n10_009": "3.2",
        "n10_008": "3.2",
        "questions": [
            {
                "num": "1",
                "question": "High availability is measured as a percentage of uptime. 'Five nines' (99.999%) allows approximately\n    _______ minutes of downtime per year. Why do small improvements in availability percentage\n    represent disproportionately large reductions in downtime?",
                "answer": "5.26 minutes. Because the percentage scale compresses at the high end — going from 99.9% to 99.99% cuts allowed downtime from ~8.7 hours to ~52 minutes, a 10x reduction for a 0.09% improvement.",
                "lines": 5
            },
            {
                "num": "2",
                "question": "HSRP (Hot Standby Router Protocol) and VRRP (Virtual Router Redundancy Protocol) both provide\n    _______ router redundancy by presenting a shared _______ IP and MAC address to clients. What\n    happens to client traffic if the active router fails?",
                "answer": "Default gateway; virtual. The standby router detects the failure and takes over the virtual IP and MAC within seconds — clients continue sending traffic to the same gateway address without reconfiguration.",
                "lines": 5
            },
            {
                "num": "3",
                "question": "In a redundant network design, a _______ point of failure is a single device or link whose failure causes\n    a complete outage. Name two common single points of failure in a school network and how redundancy\n    eliminates each.",
                "answer": "Single; examples: single uplink from access switch to core (fix: dual uplinks with EtherChannel or STP failover), single ISP connection (fix: dual ISP with BGP or failover routing), single firewall (fix: HA firewall pair).",
                "lines": 5
            },
            {
                "num": "4",
                "question": "EtherChannel (LACP) bundles multiple physical links into one logical link, increasing _______ and\n    providing _______. If one physical link in a four-link bundle fails, what percentage of bandwidth is\n    retained?",
                "answer": "Bandwidth (throughput); redundancy (link failure tolerance). 75% — three of four links remain active.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A UPS (Uninterruptible Power Supply) provides battery power during an outage long enough for a\n    _______ shutdown or _______ activation. Without a UPS, what specific type of data corruption risk\n    exists when a switch or server loses power mid-operation?",
                "answer": "Graceful; generator. File system corruption — writes that were in progress are incomplete, leaving the OS or application in an inconsistent state that may require manual repair or restore from backup.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "Recovery Time Objective (RTO) defines the maximum acceptable _______ after a failure. Recovery\n    Point Objective (RPO) defines the maximum acceptable _______ of data. A school that backs up data\n    nightly has an RPO of approximately _______ hours.",
                "answer": "Downtime (time to restore service); data loss (how old the most recent backup can be). 24 hours — if a failure occurs just before the next backup, up to one day of data could be lost.",
                "lines": 5
            },
            {
                "num": "7",
                "question": "Spanning Tree Protocol (STP) prevents _______ in redundant switched networks by blocking one or\n    more redundant ports. The tradeoff with STP redundancy is that blocked ports require _______ to\n    transition to forwarding if the active path fails.",
                "answer": "Broadcast storms (switching loops); time (STP convergence — up to 30-50 seconds with classic STP, faster with RSTP).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school's entire network goes down when a single uplink cable is accidentally\n    disconnected by a custodian. The outage lasts 45 minutes while staff locate a replacement cable.\n    Identify the design flaw, name the redundancy solution, and describe what the failure experience would\n    look like with that solution in place.",
                "answer": "Design flaw: single uplink from the access/distribution switch to the core — a single point of failure. Solution: dual uplinks with EtherChannel or STP failover. With redundancy: the second uplink carries all traffic within milliseconds of the first link going down (EtherChannel) or within seconds (RSTP failover). Users experience a brief interruption or nothing at all rather than a 45-minute outage.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "3.2.2": {
        "unit": "3.2.2",
        "title": "Load Balancing",
        "n10_009": "3.2",
        "n10_008": "3.2",
        "questions": [
            {
                "num": "1",
                "question": "A load balancer sits between _______ and a pool of _______. Clients connect to the load balancer's\n    _______ (VIP) address and never communicate directly with individual backend servers.",
                "answer": "Clients; backend servers; virtual IP (VIP) address.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Layer 4 load balancing makes forwarding decisions based on _______ and _______ — it does not\n    inspect application content. Layer 7 load balancing can inspect _______, URLs, and cookies, which\n    allows routing decisions like 'send /api/ requests to one server pool and /static/ to another.'",
                "answer": "Source/destination IP address and port numbers; HTTP headers.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Match each scheduling algorithm to its description:\n    Round robin — _______\n    Least connections — _______\n    IP hash — _______\n    Weighted round robin — _______",
                "answer": "Round robin — distribute requests sequentially across all servers; Least connections — send to the server with fewest active connections; IP hash — hash client IP to always route the same client to the same server; Weighted round robin — servers with higher weights receive proportionally more requests.",
                "lines": 5
            },
            {
                "num": "4",
                "question": "A Layer 7 health check sends an actual _______ request (e.g., GET /health) and checks the _______\n    code. Why is this more reliable than a Layer 3/4 TCP health check?",
                "answer": "HTTP request; HTTP status code (200 = healthy, 5xx = unhealthy). A TCP check only confirms the port is open — the process is running. A Layer 7 check confirms the application can actually respond correctly. A web server can accept TCP connections while returning 500 errors; only an HTTP health check catches that.",
                "lines": 6
            },
            {
                "num": "5",
                "question": "Sticky sessions (session persistence) ensure requests from the same client always reach the _______\n    backend server. Why are sticky sessions a workaround rather than an ideal solution?",
                "answer": "Same. Sticky sessions exist because the application stores session data locally on the server (in memory or disk). The ideal solution is a stateless application that stores session data in a shared backend (Redis, database) — then any server can handle any request and sticky sessions aren't needed. Sticky sessions reduce load balancing effectiveness and complicate failover.",
                "lines": 6
            },
            {
                "num": "6",
                "question": "DNS round robin assigns multiple _______ records to the same hostname. List two significant\n    limitations that make it unsuitable as the sole availability mechanism.",
                "answer": "A records (or AAAA for IPv6). Limitations: (1) No health checking — DNS keeps returning a failed server's IP until the record is manually changed or the TTL expires; (2) DNS caching means clients stick to their resolved IP for the TTL duration, so distribution is uneven and failover is slow (minutes to hours, not seconds).",
                "lines": 6
            },
            {
                "num": "7",
                "question": "Global Server Load Balancing (GSLB) distributes traffic across multiple _______ or _______. It\n    typically works through _______ — returning different IP addresses based on client location or data\n    center health.",
                "answer": "Data centers; geographic regions. It works through DNS — the GSLB system acts as the authoritative DNS resolver and returns different IPs based on geography and health status.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school's web portal is slow during exam week when all students log in\n    simultaneously. The IT team wants to add load balancing. They have three identical servers available.\n    Describe: which load balancing algorithm you would recommend, whether sticky sessions are needed,\n    and what type of health check you would configure.",
                "answer": "Algorithm: least connections — it handles variable request complexity (some students loading content, some submitting forms) better than round robin, which assumes uniform requests. Sticky sessions: depends on how the portal stores sessions. If the app stores session data in a shared database, skip sticky sessions. If it stores sessions locally, enable cookie-based sticky sessions. Health check: Layer 7 HTTP check against a /health endpoint that verifies the app and database are both responding — a TCP check isn't sufficient for an application with a database dependency.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "3.3.1": {
        "unit": "3.3.1",
        "title": "Change Management",
        "n10_009": "3.3",
        "n10_008": "3.3",
        "questions": [
            {
                "num": "1",
                "question": "Change management exists to prevent _______ changes from causing outages. Studies consistently\n    show that a majority of network outages are caused not by hardware failure but by _______.",
                "answer": "Unauthorized/uncontrolled; human error (misconfiguration, untested changes, changes made without a rollback plan).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A change request must include: a description of the change, the _______ (why it's needed), the\n    _______ window (when it will happen), and a _______ plan if the change fails or causes problems.",
                "answer": "Business justification/reason; maintenance; rollback (backout).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Changes are categorized by risk. A standard change is pre-approved and _______ risk (e.g., adding a\n    VLAN to an existing port). An emergency change bypasses normal approval because of _______.\n    What additional step is required after an emergency change is completed?",
                "answer": "Low/routine; an active incident requiring immediate resolution. Post-implementation review and retroactive documentation/approval — the change must be recorded even though it happened outside normal process.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "Before implementing any change, the current configuration should be _______ so that the rollback plan\n    has something to restore to. On a Cisco device, this is accomplished with the command _______.",
                "answer": "Backed up/saved; `copy running-config startup-config` or `copy running-config tftp://` to a remote server.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A maintenance window is a scheduled time when changes are permitted, typically during _______\n    usage hours. Why is it insufficient to simply schedule a maintenance window without also notifying\n    _______?",
                "answer": "Low (off-peak, overnight, weekend); affected users/stakeholders. Even low-traffic windows affect someone — a teacher working late, an automated backup job, a monitoring system. Notification allows users to save work and sets expectations about the planned disruption.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "A _______ review (CAB — Change Advisory Board) evaluates proposed changes before approval. In a\n    school IT context, who would typically be stakeholders in a CAB review for a major network\n    infrastructure change?\n    Answer: Change advisory; IT director, network administrator, school administrators/principals, and\n    potentially a curriculum coordinator if instructional systems are affected.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "After a change is implemented, a _______ test verifies the change worked as intended and no\n    unintended side effects occurred. What is the minimum documentation that should be recorded in the\n    change ticket when the change is complete?",
                "answer": "Post-implementation (validation/verification); actual change made, time completed, test results, any deviations from the plan, and confirmation that the rollback plan was not needed (or that it was used and what was restored).",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A network admin updates a firewall rule set on a Friday afternoon without a change\n    request, backup, or rollback plan. The change blocks access to the student grading portal. It takes until\n    Monday morning to identify and fix the problem because the admin is unreachable over the weekend.\n    Identify three change management failures and state what correct procedure would have prevented\n    each.",
                "answer": "1. No change request — a formal request would have required impact assessment identifying grading portal traffic. 2. No backup before changes — a saved pre-change config enables immediate rollback without manual troubleshooting. 3. No maintenance window or stakeholder notification — scheduling the change for a low-impact time and notifying staff ensures someone with access and knowledge is available if something breaks.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "3.3.2": {
        "unit": "3.3.2",
        "title": "Policies Procedures",
        "n10_009": "3.3",
        "n10_008": "3.3",
        "questions": [
            {
                "num": "1",
                "question": "An Acceptable Use Policy (AUP) defines what users _______ and _______ do with network resources.\n    Why must users acknowledge the AUP in writing (or digitally) rather than simply being told about it?",
                "answer": "May (are permitted to); may not (are prohibited from). Written acknowledgment creates a documented record that the user was informed of the rules — essential for disciplinary action or legal proceedings if the policy is violated.",
                "lines": 5
            },
            {
                "num": "2",
                "question": "A data classification policy assigns sensitivity levels to data. List the four common classification levels\n    from least to most sensitive and give a school network example of each.",
                "answer": "Public (school calendar, public website), Internal (staff meeting notes, curriculum materials), Confidential (student grades, personnel records), Restricted/Top Secret (financial data, SSNs, legal documents).",
                "lines": 4
            },
            {
                "num": "3",
                "question": "The principle of least privilege in access control means users receive only the permissions _______ for\n    their role. A student account that can modify grades violates this principle. What is the process called\n    when access rights are reviewed periodically to remove unnecessary permissions?",
                "answer": "Necessary/required; access review (or permission audit / user access review).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "An onboarding procedure creates accounts and grants access when a user joins. An offboarding\n    procedure _______ accounts and revokes access when a user leaves. What specific security risk does\n    a delay in offboarding create?",
                "answer": "Disables/deletes; a former employee or contractor retains valid credentials and can access systems, data, or the VPN after their authorized relationship with the organization has ended.",
                "lines": 4
            },
            {
                "num": "5",
                "question": "A password policy typically mandates minimum _______, complexity requirements, and maximum\n    _______ (how often it must be changed). Modern NIST guidance actually recommends against\n    frequent forced password changes unless there is evidence of compromise. Why?",
                "answer": "Length; age (expiration interval). Frequent forced changes cause users to choose predictable patterns (Password1! ﬁ Password2!) or write passwords down, reducing overall security rather than improving it.",
                "lines": 4
            },
            {
                "num": "6",
                "question": "A data retention policy defines how long different types of data must be kept before it can be _______.\n    Name one legal reason a school district might be required to retain student records for a specific\n    period.",
                "answer": "Destroyed/deleted; FERPA (Family Educational Rights and Privacy Act) requirements, state education records laws, or potential litigation hold requirements that mandate preserving records relevant to legal proceedings.",
                "lines": 4
            },
            {
                "num": "7",
                "question": "An incident response policy defines the steps taken when a security breach occurs: _______, _______,\n    eradication, recovery, and lessons learned. Why must the 'lessons learned' phase be documented and\n    not skipped?",
                "answer": "Preparation; identification (and containment). Without documentation, the same type of incident is likely to recur — lessons learned feed back into policy updates, control improvements, and staff training that prevent repeat breaches.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school district is audited after a data breach exposes 3,000 student records. The\n    auditors find: no AUP, no data classification policy, contractor accounts that were never deactivated,\n    and no incident response plan. For each missing policy, describe the specific harm it allowed in this\n    scenario.",
                "answer": "No AUP — no documented rules means no enforceable standard of conduct; users had no guidance on handling sensitive data. No data classification — student records were not identified as confidential, so no special protections (encryption, access controls) were applied. Undeactivated contractor accounts — a former contractor's credentials were used to access the system; offboarding procedures would have prevented this. No incident response plan — the district had no predefined steps to contain the breach, notify affected families, or preserve evidence, extending the damage and liability.",
                "real_world": True,
                "lines": 7
            },
        ]
    },
    "4.1.1": {
        "unit": "4.1.1",
        "title": "Network Security Concepts",
        "n10_009": "4.1",
        "n10_008": "4.1",
        "questions": [
            {
                "num": "1",
                "question": "The three pillars of the CIA Triad are _______, _______, and _______. Briefly define each in one\n    sentence.",
                "answer": "Confidentiality (only authorized parties can read data), Integrity (data has not been altered in transit or at rest), Availability (systems and data are accessible when needed).",
                "lines": 4
            },
            {
                "num": "2",
                "question": "A _______ is someone with authorized network access who misuses it, while a _______ is an outside\n    attacker with no prior access. Which poses the greater risk in most enterprise environments, and why?",
                "answer": "Insider threat; external threat. Insiders often pose greater risk because they already have valid credentials, know the network layout, and their activity blends with normal traffic.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "Explain the difference between a vulnerability, a threat, and a risk. Give a one-sentence example of\n    each in a network context.",
                "answer": "Vulnerability: a weakness (e.g., unpatched switch firmware). Threat: something that can exploit it (e.g., an attacker scanning for that CVE). Risk: the probability and impact if exploited (e.g., full switch compromise exposing all VLANs).",
                "lines": 5
            },
            {
                "num": "4",
                "question": "Zero-day vulnerabilities are dangerous because they have _______ available from the vendor when\n    attackers first exploit them. The primary defense while a patch is unavailable is called _______.",
                "answer": "No patches; compensating controls (e.g., firewall rules blocking the vulnerable service, disabling the feature, network segmentation).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Defense in depth means using _______ layers of security controls so that failure of any single control\n    does not result in a complete breach. Name three different layers this strategy might include.",
                "answer": "Multiple; examples include: perimeter firewall, internal segmentation, IDS/IPS, endpoint antivirus, MFA, physical locks, and user training.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "The principle of least privilege states that users and systems should have access to only what they\n    _______ to perform their job. How does this limit the damage from a compromised account?",
                "answer": "Need (minimum necessary). A compromised account with limited privileges can only access a small subset of resources, reducing the blast radius of the breach.",
                "lines": 4
            },
            {
                "num": "7",
                "question": "Network segmentation limits _______ movement by placing critical systems in separate VLANs or\n    security zones. What firewall behavior enforces the boundary between zones?",
                "answer": "Lateral; inter-VLAN firewall rules (or an internal segmentation firewall) that explicitly permit only required traffic flows and deny everything else.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school's student VLAN can reach the staff grading portal because no ACL separates\n    them. Which CIA Triad principle is most directly violated, and what single technical control would fix it?",
                "answer": "Confidentiality — student grades and staff data should not be readable by unauthorized users. Fix: an inter-VLAN ACL (or firewall rule) explicitly blocking student VLAN from reaching the staff server subnet.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "4.1.2": {
        "unit": "4.1.2",
        "title": "Common Network Attacks",
        "n10_009": "4.1",
        "n10_008": "4.1",
        "questions": [
            {
                "num": "1",
                "question": "In a man-in-the-middle (MITM) attack, the attacker positions themselves _______ two communicating\n    parties without either knowing. The attacker can both _______ and _______ the traffic.",
                "answer": "Between; intercept (read); modify (alter or inject).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "ARP poisoning enables MITM attacks by sending _______ ARP replies that map the attacker's MAC\n    address to a legitimate IP (usually the _______). This causes victim traffic to route through the attacker.",
                "answer": "Gratuitous (unsolicited); default gateway.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A Distributed Denial of Service (DDoS) attack differs from a DoS attack because it uses _______\n    sources, often a network of compromised devices called a _______. Why is this harder to block?",
                "answer": "Multiple (distributed) sources; botnet. Blocking a single IP is ineffective when thousands of different IPs are sending traffic.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A SYN flood exploits the TCP _______ handshake by sending a large number of SYN packets with\n    _______ source IPs, causing the server to hold open half-connections until its table is exhausted.",
                "answer": "Three-way; spoofed (forged).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Explain how an evil twin attack works. What makes it more convincing than a simple rogue AP with a\n    different SSID?",
                "answer": "The attacker creates an AP with the same SSID (and often same BSSID/channel) as a legitimate AP. It's convincing because the network name is identical — clients may auto-connect or be deauthenticated from the real AP and forced to the fake one.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "DNS poisoning (cache poisoning) injects _______ records into a DNS resolver's cache, redirecting\n    users to attacker-controlled IP addresses without the user changing any settings. The defense is\n    _______.",
                "answer": "Forged/malicious DNS; DNSSEC (DNS Security Extensions), which cryptographically signs records so forged responses are rejected.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "VLAN hopping using double tagging works when the attacker's port is in the same VLAN as the switch's\n    _______. The attacker sends a frame with two 802.1Q tags — the outer tag is stripped at the first\n    switch, exposing the inner tag and sending the frame to a _______.",
                "answer": "Native VLAN; different (target) VLAN.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: Users report their browser shows a certificate warning when loading the school portal,\n    but only from the library Wi-Fi. No other network has this problem. Name the most likely attack and\n    describe the two-step process an attacker used to create this symptom.",
                "answer": "Evil twin / SSL stripping or MITM with certificate substitution. Step 1: attacker sets up a rogue AP matching the school SSID in the library. Step 2: clients connect to the rogue AP; the attacker intercepts HTTPS traffic and presents their own forged certificate, causing the browser warning.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "4.1.3": {
        "unit": "4.1.3",
        "title": "Network Hardening",
        "n10_009": "4.1",
        "n10_008": "4.1",
        "questions": [
            {
                "num": "1",
                "question": "Network hardening means reducing the _______ surface by disabling unused services, ports, and\n    accounts. List three specific actions that reduce attack surface on a managed switch.",
                "answer": "Attack surface; examples: disable unused switch ports (shutdown), disable Telnet and use SSH only, change default SNMP community strings, disable CDP/LLDP on untrusted ports, enable port security.",
                "lines": 4
            },
            {
                "num": "2",
                "question": "Port security limits the number of _______ addresses allowed on a switch port. When a violation\n    occurs, the three response modes are _______ (drops frames, no alert), _______ (drops frames, logs\n    alert), and _______ (disables the port).",
                "answer": "MAC addresses; protect; restrict; shutdown (err-disable).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "802.1X uses three roles: the _______ (client device), the _______ (switch or AP that relays\n    authentication), and the _______ (RADIUS server that validates credentials). What does this prevent\n    that MAC filtering cannot?",
                "answer": "Supplicant; authenticator; authentication server. 802.1X prevents MAC spoofing attacks because it validates identity credentials, not just a hardware address that can be cloned.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "BPDU Guard protects against rogue switches being added to the network by disabling any access port\n    that receives a _______. This prevents a connected device from participating in _______ elections.",
                "answer": "BPDU (Bridge Protocol Data Unit); Spanning Tree Protocol (STP) root bridge.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "DHCP snooping builds a binding table of _______ IP-to-MAC-to-port mappings and drops DHCP\n    server messages from _______ ports. Which type of attack does this directly prevent?",
                "answer": "Legitimate/trusted; untrusted. It prevents rogue DHCP server attacks where an unauthorized device hands out malicious IP configurations.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Dynamic ARP Inspection (DAI) uses the DHCP snooping binding table to validate ARP packets. It\n    drops ARP replies where the _______ does not match the binding table entry. This defeats _______.",
                "answer": "IP-to-MAC mapping; ARP poisoning / gratuitous ARP attacks.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A network baseline documents normal behavior (traffic volumes, protocols, connection patterns) so that\n    _______ can be identified. Name two specific metrics that a baseline should capture.",
                "answer": "Anomalies (deviations from normal); examples: average bandwidth utilization per interface, typical number of active connections per host, expected DNS query volume, normal broadcast rates.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A student plugs a cheap consumer router into a classroom Ethernet jack. The router's\n    DHCP server starts handing out 192.168.1.x addresses, overriding the school's DHCP. Name the\n    attack type, the switch feature that would have prevented it, and the command category used to\n    implement it.",
                "answer": "Rogue DHCP server attack. Prevention: DHCP snooping. Implementation: configure the uplink ports to the legitimate DHCP server as trusted (`ip dhcp snooping trust`) and leave all access ports as untrusted (default), so DHCP Offer/Ack frames from the student's router are silently dropped.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "4.2.1": {
        "unit": "4.2.1",
        "title": "Firewalls And Idsips",
        "n10_009": "4.2",
        "n10_008": "4.2",
        "questions": [
            {
                "num": "1",
                "question": "A stateless firewall evaluates each packet _______, while a stateful firewall maintains a _______ table\n    that tracks active connections. Why does stateless filtering require explicit rules for return traffic?",
                "answer": "In isolation (independently); state/connection. Stateless firewalls have no memory of prior packets, so the return traffic from an outbound session looks like a new unsolicited inbound connection and must be explicitly permitted.",
                "lines": 5
            },
            {
                "num": "2",
                "question": "A next-generation firewall (NGFW) differs from a traditional stateful firewall by inspecting the _______\n    layer, allowing policy decisions based on _______ identity rather than just port number.",
                "answer": "Application; application (e.g., block BitTorrent even if it runs on port 80).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Firewalls process rules _______. If a broad deny rule appears above a specific permit rule, the permit\n    rule will _______ be reached. Best practice is to place _______ rules at the top.",
                "answer": "Top-down (first match wins); never; most specific.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "An implicit deny is a rule at the _______ of the firewall rule set that blocks all traffic not matched by a\n    preceding rule. Why is it important to _______ this rule?",
                "answer": "Bottom; log. Logging the implicit deny reveals misconfigured traffic (legitimate flows that need a rule) and attack traffic (probing or scanning).",
                "lines": 4
            },
            {
                "num": "5",
                "question": "A DMZ (demilitarized zone) places public-facing servers on a _______ network segment between the\n    internet and the internal network. If a DMZ web server is compromised, what prevents the attacker from\n    immediately reaching internal systems?",
                "answer": "Separate (isolated); firewall rules between the DMZ and the inside network limit what DMZ servers can initiate toward the internal zone — the attacker hits a second firewall barrier.",
                "lines": 4
            },
            {
                "num": "6",
                "question": "An IDS is _______ — it receives a copy of traffic and generates alerts. An IPS is _______ — traffic\n    passes through it and it can actively _______ malicious packets. What happens to network traffic if an\n    inline IPS fails in fail-closed mode?",
                "answer": "Passive; inline; drop/block. In fail-closed mode, traffic stops entirely — the network goes down but stays secure.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Signature-based detection matches traffic against _______ attack patterns, so it cannot detect\n    _______. Anomaly-based detection flags deviations from a _______ but produces more _______ than\n    signature-based systems.",
                "answer": "Known; zero-day (novel) attacks; baseline; false positives.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A network admin adds a firewall rule permitting guest VLAN traffic to the student portal\n    on port 443, but the portal remains unreachable from the guest network. The rule is syntactically\n    correct. What is the most likely cause, and how do you verify it?",
                "answer": "Rule order — a broader deny rule for the guest VLAN appears above the new permit rule, so the firewall matches it first and stops processing. Verify by reviewing the full rule set top-to-bottom and using the firewall's packet-trace or log function to see which rule is matching the traffic.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "4.2.2": {
        "unit": "4.2.2",
        "title": "Vpn And Remote Access Security",
        "n10_009": "4.2",
        "n10_008": "4.2",
        "questions": [
            {
                "num": "1",
                "question": "IPsec uses two protocols: _______ (AH) provides authentication and integrity but no encryption, and\n    _______ (ESP) provides encryption, authentication, and integrity. Which is used in modern VPN\n    deployments and why?",
                "answer": "Authentication Header; Encapsulating Security Payload. ESP is used because it provides confidentiality — without encryption, AH alone exposes the payload to eavesdropping.",
                "lines": 4
            },
            {
                "num": "2",
                "question": "IPsec tunnel mode encapsulates the _______ original IP packet inside a new IP packet. Transport\n    mode protects only the _______, leaving the original IP header visible. Which mode is standard for\n    site-to-site VPNs?",
                "answer": "Entire; payload. Tunnel mode — the VPN gateways add new outer headers to carry traffic across the internet while hiding the original source/destination.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "IKE Phase 1 establishes a _______ channel used for negotiation, authenticating peers via _______ or\n    certificates. IKE Phase 2 uses this channel to negotiate the _______ that will protect actual data traffic.",
                "answer": "Secure management (ISAKMP SA); pre-shared keys (PSK); IPsec Security Associations (SAs).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "SSL/TLS VPNs operate over TCP port _______, which makes them traverse most firewalls and NAT\n    devices easily. IPsec VPNs can struggle with NAT because NAT modifies _______, breaking IPsec's\n    integrity verification.",
                "answer": "443; IP headers.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "In a full-tunnel VPN, _______ client traffic flows through the VPN. In a split-tunnel VPN, only traffic\n    destined for _______ routes through the tunnel. What is the security tradeoff of split tunnel?",
                "answer": "All; internal (organizational) networks. Split tunnel reduces bandwidth but leaves internet-bound traffic unmonitored by the organization's security controls.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Multi-factor authentication (MFA) for VPN access requires something you _______ plus something you\n    _______. Why is username and password alone insufficient for VPN access?\n    Answer: Know (password); have (token, phone, hardware key). Credentials are frequently stolen via\n    phishing or breaches — a second factor means a stolen password alone cannot grant VPN access.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Endpoint posture checks evaluate the _______ device before granting full VPN access. List two\n    conditions a posture check might require before allowing connection.",
                "answer": "Client (connecting); examples: OS is fully patched, antivirus is installed and current, local firewall is enabled, device is domain-joined or MDM-enrolled.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A former contractor's VPN account was never deactivated. Three months after their\n    contract ended, unauthorized access to internal project files is discovered through that account. Identify\n    two process failures that allowed this and state the control that prevents each.",
                "answer": "Failure 1: No offboarding procedure to revoke VPN access — fix: documented offboarding checklist that includes immediate VPN account deactivation. Failure 2: No periodic access review to catch stale accounts — fix: quarterly account audits that remove inactive credentials.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "4.3.1": {
        "unit": "4.3.1",
        "title": "Wireless Security Threats And Defenses",
        "n10_009": "4.3",
        "n10_008": "4.3",
        "questions": [
            {
                "num": "1",
                "question": "WEP is broken because its 24-bit _______ repeats on busy networks within hours. Once an attacker\n    collects enough repeated IVs, they can mathematically recover the _______. The correct action when\n    WEP is found in production is to _______.",
                "answer": "Initialization vector (IV); encryption key. Replace it immediately — WEP provides no effective security and cannot be fixed through configuration.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "WPA replaced WEP's broken encryption with _______ (TKIP), which was designed to run on existing\n    hardware. WPA2 replaced TKIP with _______ using AES encryption. Why was TKIP considered a\n    stopgap rather than a long-term solution?",
                "answer": "TKIP (Temporal Key Integrity Protocol); CCMP. TKIP was built around the RC4 cipher WEP used, inheriting its fundamental weaknesses — it was designed for backward compatibility, not long-term security.",
                "lines": 4
            },
            {
                "num": "3",
                "question": "WPA2-Personal uses a _______ shared by all devices. WPA2-Enterprise uses individual credentials\n    authenticated via a _______ server. Why does Personal mode fail in organizational environments?",
                "answer": "Pre-shared key (PSK/passphrase); RADIUS. A shared PSK cannot be revoked for a single user — changing it requires reconfiguring every device, and compromise by one user affects all.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "WPA3-Personal replaces PSK with _______ (SAE), which provides _______ secrecy — meaning\n    previously captured traffic cannot be decrypted even if the passphrase is later compromised.",
                "answer": "Simultaneous Authentication of Equals; forward.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "802.11w Protected Management Frames (PMF) is mandatory in WPA3. It encrypts and authenticates\n    _______ frames, which defeats _______ attacks that force clients off a legitimate AP.",
                "answer": "Management (deauthentication/disassociation); deauthentication (deauth) attacks.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A WIDS passively _______ the RF environment for rogue APs and unauthorized activity. A WIPS adds\n    the ability to actively _______ rogue devices by sending deauthentication frames to clients connected\n    to them.",
                "answer": "Monitors; contain/suppress.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A captive portal intercepts _______ traffic and redirects unauthenticated clients to a login page. Name\n    two security weaknesses of captive portals that make them unsuitable as a primary security control.",
                "answer": "HTTP (unencrypted); weaknesses include: MAC address spoofing bypasses authentication, pre-authentication traffic is unencrypted on open SSIDs, and the portal only controls access — it does not encrypt ongoing sessions.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A school deploys WPA2-Personal for its staff SSID. Within a week, the passphrase\n    appears on a student group chat. IT changes the password, and it leaks again within three days.\n    Identify the root architectural problem and describe the correct solution.",
                "answer": "Root problem: WPA2-Personal uses a single shared secret that cannot be revoked per user — any one person with the password can share it. Solution: migrate to WPA2/WPA3-Enterprise with 802.1X and RADIUS authentication tied to Active Directory. Each user authenticates with their own credentials, which can be revoked individually without affecting other users.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "4.4.1": {
        "unit": "4.4.1",
        "title": "Physical Security",
        "n10_009": "4.4",
        "n10_008": "4.4",
        "questions": [
            {
                "num": "1",
                "question": "Physical access to a switch provides an attacker with _______ access, bypassing all software security\n    controls. Explain how an attacker with physical access to a Cisco switch can recover the password\n    without knowing it.",
                "answer": "Console (direct hardware); password recovery: boot into ROMMON mode, change the config register to bypass startup config, reload and set a new password — documented in Cisco's own support guides.",
                "lines": 4
            },
            {
                "num": "2",
                "question": "An access control vestibule (mantrap) prevents _______ by requiring each person to badge through a\n    first door that must _______ before the inner door can open, limiting entry to one person at a time.",
                "answer": "Tailgating (piggybacking); close/lock.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "Badge systems log every _______ with a timestamp, creating an audit trail. When an employee is\n    terminated, their badge should be disabled _______. What does tailgating defeat that a badge system\n    cannot prevent on its own?",
                "answer": "Entry (access event); immediately. Tailgating defeats the badge requirement — an authorized person opening the door provides physical access to someone who hasn't badged in.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "Server rooms require environmental monitoring for _______ (should stay between 64-75°F), _______\n    (40-60% relative humidity), and _______ detection. Why is humidity too low (below 40%) dangerous for\n    network equipment?",
                "answer": "Temperature; humidity; water (leak). Low humidity increases static electricity discharge risk, which can permanently damage sensitive electronic components.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Fire suppression in a server room must use _______ agents rather than water sprinklers. Name one\n    clean agent system used in data centers and explain why water suppression is avoided.",
                "answer": "Clean (gaseous); examples: FM-200, Novec 1230, inert gas (IG-541). Water destroys electronic equipment and creates electrical hazards — clean agents extinguish fire by removing heat or displacing oxygen without leaving residue.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "Drive disposal must match the sensitivity of the data. For standard data, _______ (multiple-pass\n    overwrite) meets most requirements. For SSDs, overwriting is unreliable because of _______, so the\n    recommended approach is _______ or physical destruction.",
                "answer": "Drive wiping (e.g., DBAN, DoD 5220.22-M); wear leveling (the controller may not overwrite every physical cell); manufacturer's secure erase command.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Degaussing uses a strong _______ field to destroy data on magnetic media. It renders the media\n    _______ (cannot be reused). Degaussing does NOT work on _______ because they store data\n    electronically, not magnetically.",
                "answer": "Magnetic; permanently unusable; SSDs (solid-state drives).",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A contractor arrives to service the HVAC system in the server room. The front desk\n    gives them a visitor badge and points them toward the server room. They enter unsupervised for 45\n    minutes. Identify two policy failures and describe the correct procedure.",
                "answer": "Failure 1: No escort — visitors in sensitive areas must be accompanied by authorized IT staff at all times. Failure 2: No access logging/sign-in for the server room entry. Correct procedure: IT staff meets the contractor at the front desk, escorts them throughout the visit, and logs entry/exit time and purpose in the access record.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "4.4.2": {
        "unit": "4.4.2",
        "title": "Data Loss Prevention",
        "n10_009": "4.4",
        "n10_008": "4.4",
        "questions": [
            {
                "num": "1",
                "question": "DLP addresses data in three states. Match each state to its description:\n    Data at _______ — stored on a device or server, protected primarily by encryption and access controls.\n    Data in _______ — being transmitted across a network, vulnerable to interception or misdirection.\n    Data in _______ — actively open or displayed, vulnerable to screen capture, clipboard copying, or\n    printing.",
                "answer": "Data at rest; data in motion; data in use.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A DLP system uses two primary identification methods:\n    _______ inspection examines the actual file contents for patterns like SSN formats, credit card\n    numbers, or keywords.\n    _______ awareness evaluates who is sending data, where it is going, and what application is being\n    used — regardless of content.",
                "answer": "Content inspection; context awareness.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "A guidance counselor emails a spreadsheet containing IEP records to a teacher's personal Gmail\n    account. Which federal regulation does this most directly violate, and why?\n    _________________________________________\n    _________________________________________\n    _________________________________________",
                "answer": "FERPA (Family Educational Rights and Privacy Act). FERPA requires schools receiving federal funding to control access to and disclosure of student education records. Sending IEP records to a personal, non-district email address is an unauthorized disclosure of protected student records.",
                "lines": 5
            },
            {
                "num": "4",
                "question": "Endpoint DLP can enforce controls directly on a user's device. List three specific endpoint DLP controls\n    described in the lesson:\n    1. _______________________________________\n    2. _______________________________________\n    3. _______________________________________",
                "answer": "Any three of: (1) USB drive blocking — prevents writes to removable media; (2) Clipboard controls — blocks copy/paste from protected apps to unprotected ones; (3) Print controls — prevents printing sensitive documents without authorization; (4) Screen capture controls — blocks Print Screen when protected apps are in focus.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "Network DLP requires _______ inspection to function effectively in modern environments. Without it,\n    the DLP appliance can only see _______ blobs for most outbound traffic. What performance and\n    privacy tradeoff does enabling this create?",
                "answer": "SSL/TLS inspection; encrypted blobs. The appliance must decrypt, inspect, re-encrypt, and forward every HTTPS session — introducing processing overhead, latency, and privacy concerns because the organization can now read all encrypted employee communications.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "A _______ (CASB) sits between users and cloud services to enforce DLP policies on cloud-hosted\n    data. Explain why on-premise network DLP is insufficient when teachers access Google Drive from\n    home.",
                "answer": "Cloud Access Security Broker (CASB). When a teacher accesses Google Drive from home, traffic travels between their home network and Google's servers — it never crosses the school's network boundary. The on-premise DLP appliance never sees the traffic, so it cannot inspect or block it. A CASB enforces policy regardless of the user's physical location.",
                "lines": 6
            },
            {
                "num": "7",
                "question": "Data _______ assigns sensitivity labels such as Public, Internal, Confidential, and Restricted to data.\n    DLP rules then reference these labels to apply appropriate controls. Why does this system often fail in\n    practice, even when the technology works correctly?",
                "answer": "Data classification. It fails because classification requires consistent, disciplined behavior from every user who creates or handles data — people must actually label things correctly. Manual classification relies on user training and compliance, which are inherently inconsistent. The technology enforces the label; the human applies it.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A user emails a sensitive spreadsheet as a password-protected ZIP file. The network\n    DLP system allows it through without flagging it. A colleague complains that DLP is blocking legitimate\n    encrypted emails to a vendor. Identify both failure modes and explain the tradeoff the security team\n    faces when deciding how to handle encrypted outbound attachments.",
                "answer": "First scenario: encryption bypass failure mode — content inspection cannot read inside a password-protected archive, so the sensitive data leaves undetected. Second scenario: false positive — blocking all encrypted attachments prevents legitimate secured communications. The tradeoff: allow encrypted attachments (risk data exfiltration via encryption bypass) vs. block all encrypted attachments (disrupt legitimate encrypted workflows). Most organizations choose a middle path: block unknown encrypted archives but allow organizationally-managed encrypted email.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "5.1.1": {
        "unit": "5.1.1",
        "title": "Troubleshooting Methodology",
        "n10_009": "5.1",
        "n10_008": "5.1",
        "questions": [
            {
                "num": "1",
                "question": "List the CompTIA seven-step troubleshooting methodology in order.\n    1. _______\n    2. _______\n    3. _______\n    4. _______\n    5. _______\n    6. _______\n    7. _______",
                "answer": "1. Identify the problem. 2. Establish a theory of probable cause. 3. Test the theory to determine the cause. 4. Establish a plan of action. 5. Implement the solution or escalate. 6. Verify full system functionality and implement preventive measures. 7. Document findings, actions, and outcomes.",
                "lines": 5
            },
            {
                "num": "2",
                "question": "Step 1 says to 'question the obvious.' Give an example of an obvious check that resolves a surprising\n    number of network tickets — and explain why it's easy to skip.",
                "answer": "Examples: Is the cable plugged in? Is the port administratively shut down? Is the device powered on? These are easy to skip because they feel beneath a trained technician — but they resolve a significant percentage of real tickets.",
                "lines": 5
            },
            {
                "num": "3",
                "question": "Why is Step 3 (test the theory) separated from Step 5 (implement the solution)? What mistake happens\n    when a technician combines testing and implementing?",
                "answer": "Testing confirms the cause through observation without changing anything. If a technician changes the config to 'test' whether that fixes it, they may introduce a second problem, lose the ability to roll back, or fix a symptom without identifying the actual cause.",
                "lines": 5
            },
            {
                "num": "4",
                "question": "Step 4 requires establishing a plan before implementing. A good plan includes: the action to take, the\n    expected _______, what to check to confirm success, and a _______ plan if the change doesn't work.",
                "answer": "Outcome/result; rollback.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "Bottom-up troubleshooting starts at Layer _______ and works upward. This approach guarantees you\n    don't miss a lower-layer problem masquerading as a higher-layer issue. The tradeoff is _______ — it\n    checks many layers before reaching the actual problem.\n    Answer: 1 (Physical); speed/efficiency.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Divide-and-conquer troubleshooting typically starts at Layer _______. If the device can ping its\n    _______ successfully, you know Layers 1-3 are likely working and you focus upward. If not, you focus\n    downward.",
                "answer": "3 (Network); default gateway.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Step 7 — documentation — is often skipped. Name two concrete negative outcomes that happen when\n    documentation is absent from the troubleshooting process.",
                "answer": "Examples: the next technician who encounters the same issue starts from scratch, wasting time; recurring problems are never identified as recurring because there is no history; institutional knowledge exists only in one person's memory and is lost when they leave.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: A tech gets a ticket that second-floor users can't reach the internet. They assume it's\n    the uplink cable (same problem last week), swap it, and leave. Fifteen minutes later, the ticket reopens.\n    Identify which step they skipped and what the correct process would have revealed.",
                "answer": "Skipped Step 1 (information gathering) and Step 2 (forming and ranking theories). Correct process: check the switch for error messages — in this case, the uplink port was err-disabled by a loop that appeared an hour earlier. The cable was never the problem.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "5.1.2": {
        "unit": "5.1.2",
        "title": "Troubleshooting Tools",
        "n10_009": "5.1",
        "n10_008": "5.1",
        "questions": [
            {
                "num": "1",
                "question": "The `ping` command sends _______ Echo Request packets and listens for _______ replies. A\n    'Request timed out' means no reply came back, while 'Destination host unreachable' means _______\n    explicitly reported the host is not reachable.",
                "answer": "ICMP; Echo; a router along the path.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "In ping output, the TTL value tells you approximately how many _______ the packet traversed. If you\n    ping a Linux host and receive TTL=56, approximately _______ hops separated you from the\n    destination.",
                "answer": "Hops (routers); 8 hops (Linux starts TTL at 64; 64 - 56 = 8).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "`traceroute`/`tracert` maps the Layer 3 path by sending packets with incrementing _______ values.\n    When a packet's TTL reaches zero, the router sends back a _______ message revealing its IP\n    address.",
                "answer": "TTL (Time to Live); ICMP Time Exceeded.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "You run `nslookup portal.school.edu` and the Server line shows `10.1.1.5`. You then run `nslookup\n    portal.school.edu 8.8.8.8` and get a different IP. What does this indicate, and what should you\n    investigate?",
                "answer": "The client's configured DNS server (10.1.1.5) is returning an incorrect record for that hostname. This could be DNS poisoning, a misconfigured zone file, or cache corruption. Investigate the DNS server's zone records and cache.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "A workstation running Windows shows a 169.254.x.x address in `ipconfig /all`. This is called _______\n    and means the client _______ to receive a DHCP lease. List two possible causes.",
                "answer": "APIPA (Automatic Private IP Addressing); failed. Causes: DHCP server is down, no IP helper-address (relay) on the gateway, DHCP scope is exhausted, or the client is on the wrong VLAN with no DHCP server.",
                "lines": 5
            },
            {
                "num": "6",
                "question": "`netstat -an` shows the state LISTENING on port 443 and ESTABLISHED on port 3306. What do these\n    states tell you, and what two services are most likely running?\n    Answer: LISTENING means a service is waiting for inbound connections on that port — port 443\n    means a web server (HTTPS) is running. ESTABLISHED means an active TCP session exists — port\n    3306 is MySQL, so the host has an active database connection.",
                "answer": "",
                "lines": 3
            },
            {
                "num": "7",
                "question": "In Wireshark, _______ filters limit what is captured (set before capture begins), while _______ filters\n    limit what is displayed from an existing capture. If you suspect ARP poisoning, what display filter and\n    what pattern would you look for?",
                "answer": "Capture filters; display filters. Filter: `arp`. Look for: gratuitous ARP replies (responses sent without a request) where multiple different MAC addresses are claiming the same IP — especially the gateway's IP.",
                "lines": 5
            },
            {
                "num": "8",
                "question": "REAL WORLD: You are given a fiber optic cable from a patch panel to an AP that has no link light. You\n    clean the connectors, verify the SFP types match, and verify the AP is powered. The link still won't\n    come up. Name the hardware tool you use next, what it measures, and what result would tell you the\n    cable has a break and where.",
                "answer": "OTDR (Optical Time-Domain Reflectometer). It sends light pulses down the fiber and measures reflections, calculating attenuation and the distance to each event. A sharp drop in the trace at a specific distance (e.g., at 23 meters) indicates a break or severe bend at that point in the cable run.",
                "real_world": True,
                "lines": 5
            },
        ]
    },
    "5.2.1": {
        "unit": "5.2.1",
        "title": "Troubleshooting Cables And Physical Layer",
        "n10_009": "5.2",
        "n10_008": "5.2",
        "questions": [
            {
                "num": "1",
                "question": "A split pair passes a basic continuity test because pin-to-pin connectivity is _______, but the two\n    conductors are not properly _______ together, destroying interference cancellation. Only a _______\n    tester that measures crosstalk will catch it.",
                "answer": "Correct; twisted (paired); certification.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Attenuation is measured in _______ and increases with cable _______. The maximum recommended\n    run length for Cat6 copper cable is _______ meters total (including patch cables at each end).",
                "answer": "Decibels (dB); length (and temperature); 100 meters.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "NEXT (Near-End Crosstalk) is caused by signal coupling between pairs at the _______ end of the\n    cable. The most common installation cause is untwisting more than _______ of wire at the connector\n    termination.",
                "answer": "Transmitting (near/source); half an inch (about 13mm).",
                "lines": 3
            },
            {
                "num": "4",
                "question": "Data cables running parallel to power cables should maintain at least _______ of separation. Where\n    they must cross, they should cross at _______ to minimize electromagnetic coupling. If separation is\n    impossible, use _______ cabling.",
                "answer": "12 inches (30cm); 90 degrees; STP (shielded twisted pair).",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A PoE port that repeatedly powers a device on and off is likely due to insufficient _______ on the\n    switch. A device spec'd for 802.3at (PoE+, _______ watts) will fail on a switch that only supports\n    802.3af (_______ watts).",
                "answer": "Power budget; 30W; 15.4W.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "Fiber optic bend radius violations occur when cable is bent tighter than the minimum specification,\n    causing _______ to escape the fiber core (macrobending). The tool that makes these leaks visible is a\n    _______.",
                "answer": "Light; visual fault locator (VFL).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "A switch port with a green link light but rising CRC error counts in `show interface` output indicates a\n    _______ layer problem. Name three symptoms a user might report that actually trace back to CRC\n    errors.",
                "answer": "Physical (Layer 1); symptoms: slow file transfers, dropped VoIP calls, intermittent connection timeouts, video buffering, high retransmission rates.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A newly installed patch panel in a wiring closet works for most ports, but four ports on\n    one patch strip have poor throughput and high error rates at gigabit speeds, while basic link works fine\n    at 100 Mbps. The cable runs are all under 15 meters. What is the most likely cause and how do you\n    confirm it?",
                "answer": "Split pairs on those four terminations — the conductor pairs were not punched down in the correct T568A or T568B sequence, so the twist pairing is broken. Basic link negotiates because continuity is intact, but gigabit (which uses all four pairs) exposes the crosstalk. Confirm with a certification tester measuring NEXT on each affected port.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "5.2.2": {
        "unit": "5.2.2",
        "title": "Troubleshooting Network Connectivity",
        "n10_009": "5.2",
        "n10_008": "5.2",
        "questions": [
            {
                "num": "1",
                "question": "A workstation has IP address 169.254.45.3. This tells you the client _______ to contact a DHCP server.\n    The client self-assigned an _______ address. From this state, the client can communicate with\n    _______ but nothing else.",
                "answer": "Failed; APIPA (Automatic Private IP Addressing / link-local). Other APIPA hosts on the same local segment.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Two devices have the same IP address on the same VLAN. Describe the symptom a user would\n    experience and name the command on the affected client that might reveal a changing MAC address\n    for the gateway.",
                "answer": "Intermittent connectivity — sessions work for moments then drop as ARP responses alternate between the two devices' MACs. Command: `arp -a` (the gateway's MAC entry flips between two different values).",
                "lines": 4
            },
            {
                "num": "3",
                "question": "Complete the four-step diagnostic sequence for 'I can't get to the internet.'\n    Step 1: `ping _______` — tests local Layer 3 connectivity.\n    Step 2: `ping _______` — tests internet path by IP, bypassing DNS.\n    Step 3: `nslookup _______` — tests DNS resolution.\n    Step 4: If Step 2 works but Step 3 fails, the problem is _______.",
                "answer": "Step 1: ping . Step 2: ping 8.8.8.8 (or any public IP). Step 3: nslookup google.com (any public domain). Step 4: DNS failure.",
                "lines": 4
            },
            {
                "num": "4",
                "question": "A client can ping the gateway and external IPs but cannot reach port 443 on an internal server.\n    `Test-NetConnection 10.1.50.10 -Port 443` returns a timeout. What are two possible causes?",
                "answer": "A network firewall rule is blocking TCP 443 to that server; or the Windows Firewall on the destination server is blocking inbound 443; or the service (web server) is not running on that host.",
                "lines": 5
            },
            {
                "num": "5",
                "question": "A VLAN that exists on an access switch but is not added to the _______ between that switch and the\n    distribution layer will have Layer 2 connectivity locally but cannot reach the _______. Clients will appear\n    to have valid IPs but go nowhere.",
                "answer": "Trunk (allowed VLAN list); default gateway / rest of the network.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "NAT misconfiguration can cause internal hosts to send packets to the internet with _______ source\n    addresses that are dropped by ISP routers. A new subnet that wasn't added to the NAT _______ list is\n    the most common cause after a VLAN expansion.",
                "answer": "Private (RFC 1918); access control list (ACL) / NAT pool.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "Multiple users on one switch cannot reach the internet, but users on other switches are fine. The uplink\n    from that switch shows _______ in `show interface`. What is the most efficient next step to narrow the\n    cause?",
                "answer": "Err-disabled (or down/down); investigate why the uplink err-disabled — check switch logs for the error type (BPDU guard, port security violation, loop detection) before re-enabling.",
                "lines": 4
            },
            {
                "num": "8",
                "question": "REAL WORLD: A teacher moves to a new classroom. Their laptop has the correct IP, gateway, and\n    DNS. They can ping the gateway. They can ping 8.8.8.8. But no websites load. Nslookup for any public\n    domain returns the correct IP. Describe what you would check next and why.",
                "answer": "The DNS and network path are working. The next check is a firewall rule — try `Test-NetConnection google.com -Port 443` and port 80. If both time out, a network firewall is likely blocking outbound HTTP/HTTPS from the new classroom's port or VLAN. Check whether the port is in the correct VLAN and whether the VLAN has outbound permit rules for ports 80 and 443.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "5.3.1": {
        "unit": "5.3.1",
        "title": "Troubleshooting Wireless Issues",
        "n10_009": "5.3",
        "n10_008": "5.3",
        "questions": [
            {
                "num": "1",
                "question": "Signal strength is measured in _______ (always negative — closer to zero is stronger). -30 dBm is\n    excellent. -67 dBm is the minimum for reliable VoIP. Below _______ dBm, retransmissions spike and\n    connectivity becomes unreliable.",
                "answer": "dBm (decibels relative to one milliwatt); -80 dBm.",
                "lines": 3
            },
            {
                "num": "2",
                "question": "Signal-to-Noise Ratio (SNR) is the difference between _______ strength and the _______ floor. A\n    client with -40 dBm signal but a noise floor of -42 dBm has an SNR of _______ dB, which is nearly\n    unusable despite strong signal.",
                "answer": "Signal; noise; -2 dB (or approximately 2 dB).",
                "lines": 3
            },
            {
                "num": "3",
                "question": "In the 2.4 GHz band, only channels _______, _______, and _______ are non-overlapping. Using\n    channels 3 or 8 causes _______ interference that is worse than co-channel interference because the\n    APs can't properly defer to each other.",
                "answer": "1; 6; 11; adjacent channel.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "A 'sticky client' stays associated with a distant AP despite a nearby AP having much stronger signal.\n    The roaming decision is made by the _______, not the AP. Three 802.11 amendments that improve\n    roaming are 802.11_____ (fast BSS transition), 802.11_____ (neighbor reports), and 802.11_____\n    (AP-directed roaming).",
                "answer": "Client (Wi-Fi adapter/driver); 802.11r; 802.11k; 802.11v.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "An AP rated for 10 Gbps of stateful throughput might only deliver 2 Gbps with TLS inspection and IPS\n    enabled because deeper inspection requires more _______. In a wireless context, each AP has a\n    practical client limit — adding more clients causes _______ rather than coverage failure.",
                "answer": "Processing power (CPU/memory); capacity degradation (airtime contention).",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A microwave oven operates at _______ GHz, directly overlapping the _______ GHz Wi-Fi band. This\n    causes _______ interference that lasts as long as the microwave runs. The best mitigation is to steer\n    clients to the _______ GHz band.",
                "answer": "2.45; 2.4; non-Wi-Fi (external RF); 5 GHz.",
                "lines": 3
            },
            {
                "num": "7",
                "question": "On Windows, the command _______ displays the current BSSID, channel, signal strength, and radio\n    type for the active wireless connection. This tells you which specific AP radio the client is connected to,\n    which is useful for diagnosing _______ problems.",
                "answer": "`netsh wlan show interfaces`; wrong AP association / sticky client / band steering.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: The school auditorium has one AP on the ceiling. During regular periods it works fine.\n    During assemblies with 300 students, the wireless network is dead — not slow, completely\n    unresponsive. Signal strength readings from the floor are excellent at -45 dBm. Identify the problem\n    and the correct solution.",
                "answer": "Capacity problem, not a coverage problem. The single AP cannot serve 300 simultaneous clients — airtime contention grinds throughput to zero even though signal is strong. Solution: deploy additional APs at reduced transmit power (smaller cells, fewer clients per AP). Do not increase transmit power on the existing AP — that makes the problem worse by extending the cell without adding capacity.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
    "5.3.2": {
        "unit": "5.3.2",
        "title": "Troubleshooting Network Security Issues",
        "n10_009": "5.3",
        "n10_008": "5.3",
        "questions": [
            {
                "num": "1",
                "question": "ARP poisoning and a duplicate IP address both produce intermittent connectivity and changing ARP\n    cache entries. The key difference in `arp -a` output: duplicate IP shows two MACs _______ for the\n    same IP, while ARP poisoning shows the _______ IP being claimed by an attacker's MAC.",
                "answer": "Competing / alternating; gateway's (default gateway).",
                "lines": 3
            },
            {
                "num": "2",
                "question": "A rogue DHCP server is detected when a client's `ipconfig /all` shows a _______ field listing an IP that\n    is not your legitimate DHCP server. On the switch, the command _______ can identify which port the\n    rogue device's MAC is connected to.",
                "answer": "DHCP Server; `show mac address-table address `.",
                "lines": 3
            },
            {
                "num": "3",
                "question": "To verify DNS hijacking, run `nslookup ` against your configured DNS server, then run the same query\n    against _______ (a known-good external resolver). If the results _______, your local DNS server is\n    returning malicious or incorrect records.",
                "answer": "8.8.8.8 (or 1.1.1.1 or any trusted public resolver); differ.",
                "lines": 3
            },
            {
                "num": "4",
                "question": "In firewall logs, a vertical port scan appears as one _______ IP hitting _______ destination ports on the\n    same host in rapid succession. A horizontal scan appears as one source IP hitting the _______ port\n    across many different destination IPs.",
                "answer": "Source; sequential (many different); same.",
                "lines": 3
            },
            {
                "num": "5",
                "question": "A compromised host may show three behavioral indicators in network data: (1) unexpectedly _______\n    outbound traffic volume, (2) connections to _______ or rotating external IP addresses not associated\n    with known services, and (3) DNS queries for randomly generated _______ names (DGA).",
                "answer": "High; unusual / unfamiliar; domain.",
                "lines": 3
            },
            {
                "num": "6",
                "question": "A certificate warning showing 'certificate issued by untrusted authority' on a site that normally loads\n    cleanly may indicate a _______ attack where an attacker is presenting a forged certificate. This\n    warning should trigger immediate _______ rather than clicking through.",
                "answer": "Man-in-the-middle (MITM) / SSL interception; investigation (escalation to security team).",
                "lines": 3
            },
            {
                "num": "7",
                "question": "When a suspected compromised host is identified, the first response action is to _______ the device\n    from the network. You should NOT _______ the device, as this destroys volatile memory that may\n    contain forensic evidence.",
                "answer": "Isolate / disconnect (disable the switch port or disconnect Wi-Fi); reboot.",
                "lines": 3
            },
            {
                "num": "8",
                "question": "REAL WORLD: A teacher reports their browser keeps redirecting to unfamiliar sites when accessing\n    the school portal. The network team confirms connectivity is fine and ping works. Help desk clears the\n    browser cache twice with no improvement. Describe the three diagnostic commands that would identify\n    the root cause within five minutes.",
                "answer": "1. `ipconfig /all` — check the DHCP Server field; if it shows an unexpected IP, a rogue DHCP server is the source. 2. `nslookup portal.school.edu` — check the responding DNS server; if it's not the school's server, DNS is being redirected. 3. `nslookup portal.school.edu 8.8.8.8` — compare results from a trusted resolver; if the IPs differ, the local DNS is returning hijacked records. Root cause: rogue DHCP server pushing a malicious DNS address.",
                "real_world": True,
                "lines": 6
            },
        ]
    },
