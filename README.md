
# wgwarden
**Offline WireGuard Static Mesh Manager & Generator.** Keep and update all your WireGuard configs in one place; export (auto) updated config files locally.

*Sunday Morning Vibecoded tool—simple, effective, no bloat.*

---

### What is this for?
(Re)generate **Static Mesh** or **Hybrid/Partial Mesh** configs for your WireGuard peers. 

It is designed for those who want a reliable, plain WireGuard setup without any background overhead (SDN controllers), but also don't want to manually track and update `AllowedIPs` across every peer every time a change is made.

### Core Features
* **Single Source of Truth:** Manage multiple independent WireGuard networks within a single portable JSON file.
* **Automated Allowlists:** Define a peer’s local network once; wgwarden automatically injects it into the `AllowedIPs` of all linked peers.
* **Instant Reflect:** Any changes to a peer (IPs, keys, or networks) are instantly reflected across the entire configuration.
* **Flexible Topology:** Use it for anything from a **simple 1:1 tunnel** to a **complex N:N Full Mesh**.
* **Built-in Tools:** Generates valid WireGuard Keypairs and QR Codes for mobile exports.
* **Portable:** No installation required. Stores data in a simple JSON file in the same directory.

<img width="1153" height="934" alt="image" src="https://github.com/user-attachments/assets/b262f1af-14a0-491f-98a5-826e8073c0de" />

---

### How to use:
1.  **Define a Peer:** Enter the keys and the **Local Network list** (the IPs/Subnets this peer "owns" or provides access to).
2.  **Link Peers:** Select which peers should connect. Linking Peer A to Peer B automatically handles the `AllowedIPs` exchange for both.
3.  **Export:** Click on a peer to export via **QR Code**, **File**, or **Copy/Paste**. 

> **Tip on Copying:** To copy a config, simply **Rename** it. The tool will save a new entry with the new name and keep the original in place. 

---

### Security & Logic
* **Plaintext Storage:** The JSON file is **not encrypted**. Keep it secure (e.g., on an encrypted volume).
* **Manual Oversight:** The tool does NOT check for IP overlaps by design, allowing you to create flexible or duplicate configs for different scenarios.
* **Offline:** No data leaves your machine. 

---

### Use Cases
* **Simple Networks:** Use as a vault for basic Point-to-Point links.
* **Full Mesh (N:N):** Connect every device to every other device without the manual config math.
* **Hybrid Mesh:** Easily manage "Hub and Spoke" setups where only certain peers can see each other.
