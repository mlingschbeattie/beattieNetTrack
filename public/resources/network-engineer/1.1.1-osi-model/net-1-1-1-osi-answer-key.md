# OSI Model — Guided Notes ANSWER KEY

**Unit 1.1.1 | CompTIA Network+ N10-009 Objective 1.1**

---

1. The OSI model divides network communication into **seven (7)** layers, from the **Physical** layer at the bottom to the **Application** layer at the top.

2. Layer 1 devices — such as hubs, repeaters, and **network interface cards (NICs)** — deal only with raw **bits (electrical signals, light pulses, or radio waves)** and have no understanding of addresses or protocols.

3. A switch operates at Layer **2 (Data Link)** and uses **MAC** addresses to forward frames to the correct port, rather than flooding traffic to every device like a hub.

4. A **MAC address** is a hardware address burned into a network adapter, used at **Layer 2 (Data Link)** to deliver frames between devices on the same local network. An **IP address** is a logical address used at **Layer 3 (Network)** to route packets across different networks. MAC addresses work locally; IP addresses work across the internet.

5. At Layer 4, the two main transport protocols are **TCP (Transmission Control Protocol)** and **UDP (User Datagram Protocol)**. The first provides reliable, ordered delivery; the second prioritizes **speed** over reliability.

6. Port numbers exist at Layer **4 (Transport)**. They allow a single device with one IP address to run multiple **services (or applications)** simultaneously (for example, a web server and an SSH daemon on the same machine).

7. When a browser negotiates a TLS connection to load an HTTPS website, which OSI layer handles that encryption setup? **Layer 6 (Presentation)**

8. **Real World:** Since the user can ping an external IP address (`8.8.8.8`), Layers 1 through 3 are working — the physical connection is good, the switch is forwarding traffic, and IP routing is functional. The problem is most likely **DNS (Domain Name System)**, which operates at **Layer 7 (Application)**. The computer can reach the internet by IP but cannot translate domain names into IP addresses, so the browser has no IP to connect to. The fix would be to check the DNS server configuration (e.g., `nslookup` returning a timeout confirms this) and correct or replace the DNS server address.

---

*Place this file on the class server so students can retrieve it after completing the notes.*
