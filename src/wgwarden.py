import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import json
import os
import base64
import qrcode # pip install qrcode[pil]
from PIL import ImageTk

# Native Key Generation
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(SCRIPT_DIR, "wireguard_warden.json")

class WGWarden:
    def __init__(self, root):
        self.root = root
        self.root.title("WireGuard Warden")
        self.root.geometry("1150x900")
        self.root.configure(bg="#2c3e50")
        
        self.data = self.load_data()
        self.current_peer_id = None
        
        self.setup_ui()
        self.refresh_peer_list()

    def load_data(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r", encoding='utf-8') as f: return json.load(f)
            except: return {"peers": {}}
        return {"peers": {}}

    def save_data(self):
        try:
            with open(DB_FILE, "w", encoding='utf-8') as f: json.dump(self.data, f, indent=4)
        except PermissionError:
            messagebox.showerror("Error", "Permission Denied.")

    def generate_keys(self):
        try:
            priv_key = x25519.X25519PrivateKey.generate()
            priv_bytes = priv_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption()
            )
            pub_bytes = priv_key.public_key().public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw
            )
            self.priv_key_var.set(base64.b64encode(priv_bytes).decode('utf-8'))
            self.pub_key_var.set(base64.b64encode(pub_bytes).decode('utf-8'))
        except Exception as e:
            messagebox.showerror("Keygen Error", f"Ensure 'cryptography' is installed: {e}")

    def setup_ui(self):
        # LEFT PANEL
        left_panel = tk.Frame(self.root, width=250, bg="#1a252f", padx=5, pady=5)
        left_panel.pack(side="left", fill="y")
        tk.Label(left_panel, text="PEERS", fg="#ecf0f1", bg="#1a252f", font=("Arial", 12, "bold")).pack(pady=15)
        self.peer_listbox = tk.Listbox(left_panel, font=("Consolas", 11), bg="#34495e", fg="white", borderwidth=0, highlightthickness=0, selectbackground="#3498db")
        self.peer_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.peer_listbox.bind("<<ListboxSelect>>", self.on_select_peer)
        tk.Button(left_panel, text="+ NEW PEER", command=self.new_peer, bg="#27ae60", fg="white", relief="flat", font=("Arial", 10, "bold"), pady=8).pack(fill="x", padx=5, pady=10)

        # RIGHT PANEL
        self.edit_frame = tk.Frame(self.root, padx=30, pady=20, bg="#2c3e50")
        self.edit_frame.pack(side="right", fill="both", expand=True)

        r = 0
        tk.Label(self.edit_frame, text="Peer Identity", fg="#3498db", bg="#2c3e50", font=("Arial", 14, "bold")).grid(row=r, column=0, sticky="w", pady=(0,10))
        
        r += 1
        fields = [("Internal Name:", "name"), ("VPN IP (CIDR):", "vpn_ip"), ("DNS Server:", "dns"), ("Public Key:", "pub_key"), ("Private Key:", "priv_key"), ("Endpoint (IP:Port):", "endpoint")]
        for lbl_text, var_name in fields:
            tk.Label(self.edit_frame, text=lbl_text, fg="#bdc3c7", bg="#2c3e50", font=("Arial", 10)).grid(row=r, column=0, sticky="w", pady=3)
            setattr(self, f"{var_name}_var", tk.StringVar())
            entry_frame = tk.Frame(self.edit_frame, bg="#2c3e50")
            entry_frame.grid(row=r, column=1, sticky="ew", padx=10)
            ent = tk.Entry(entry_frame, textvariable=getattr(self, f"{var_name}_var"), bg="#34495e", fg="white", insertbackground="white", borderwidth=0, highlightthickness=1, highlightbackground="#1a252f", relief="flat")
            ent.pack(side="left", fill="x", expand=True)
            if var_name == "priv_key":
                tk.Button(entry_frame, text="GEN", command=self.generate_keys, bg="#f39c12", fg="white", font=("Arial", 7, "bold"), relief="flat", padx=10).pack(side="right", padx=(5,0))
            if var_name == "endpoint": self.endpoint_ent = ent
            r += 1

        self.is_dynamic_var = tk.BooleanVar()
        tk.Checkbutton(self.edit_frame, text="Dynamic/Mobile (Handshake Initiator Only)", variable=self.is_dynamic_var, command=self.toggle_dynamic, bg="#2c3e50", fg="#ecf0f1", activebackground="#2c3e50", selectcolor="#1a252f", activeforeground="white").grid(row=r, column=1, sticky="w")

        r += 1
        list_container = tk.Frame(self.edit_frame, bg="#2c3e50")
        list_container.grid(row=r, column=0, columnspan=2, sticky="nsew", pady=20)
        self.edit_frame.rowconfigure(r, weight=1)

        self.local_net_ui = self.create_vertical_list(list_container, "LOCAL NETWORKS", 0, self.add_network)
        self.links_ui = self.create_vertical_list(list_container, "LINKED PEERS", 1, self.show_link_picker)

        r += 1
        footer = tk.Frame(self.edit_frame, bg="#2c3e50")
        footer.grid(row=r, column=0, columnspan=2, pady=10)
        for text, color, cmd in [(" SAVE ", "#27ae60", self.save_current), (" EXPORT ", "#2980b9", self.export_config), (" QR CODE ", "#8e44ad", self.export_qr), (" DELETE ", "#c0392b", self.delete_peer)]:
            tk.Button(footer, text=text, bg=color, fg="white", width=12, relief="flat", font=("Arial", 9, "bold"), command=cmd).pack(side="left", padx=8)
        self.edit_frame.columnconfigure(1, weight=1)

    def create_vertical_list(self, parent, title, col, add_cmd):
        outer_frame = tk.Frame(parent, bg="#1a252f", padx=5, pady=5) 
        outer_frame.pack(side="left", fill="both", expand=True, padx=5)
        tk.Label(outer_frame, text=title, bg="#1a252f", fg="#3498db", font=("Arial", 9, "bold")).pack(pady=(0, 5))
        lb = tk.Listbox(outer_frame, height=10, bg="#2c3e50", fg="white", borderwidth=0, highlightthickness=0, font=("Consolas", 10))
        lb.pack(fill="both", expand=True)
        btn_frame = tk.Frame(outer_frame, bg="#1a252f")
        btn_frame.pack(fill="x", pady=(10, 0))
        btn_opt = {"bg": "#34495e", "fg": "white", "relief": "flat", "font": ("Arial", 8, "bold"), "pady": 5}
        tk.Button(btn_frame, text="+ ADD", command=lambda: add_cmd(lb), **btn_opt).pack(side="left", expand=True, fill="x")
        tk.Frame(btn_frame, width=10, bg="#1a252f").pack(side="left")
        tk.Button(btn_frame, text="- REMOVE", command=lambda: lb.delete(tk.ANCHOR), **btn_opt).pack(side="left", expand=True, fill="x")
        return lb

    def add_network(self, lb):
        val = simpledialog.askstring("Input", "Enter Subnet:")
        if val: lb.insert("end", val.strip())

    def show_link_picker(self, lb):
        current_name = self.name_var.get().strip()
        options = [p for p in self.data["peers"].keys() if p != current_name and p not in list(lb.get(0, "end"))]
        if not options: return
        picker = tk.Toplevel(self.root, bg="#1a252f")
        plist = tk.Listbox(picker, font=("Consolas", 10), bg="#2c3e50", fg="white", borderwidth=0)
        plist.pack(fill="both", expand=True, padx=10, pady=10)
        for o in options: plist.insert("end", o)
        def pick():
            if plist.curselection(): lb.insert("end", plist.get(plist.curselection())); picker.destroy()
        tk.Button(picker, text="Link", command=pick, bg="#27ae60", fg="white", relief="flat").pack(pady=5)

    def toggle_dynamic(self):
        state = self.is_dynamic_var.get()
        bg_color = "#1a252f" if state else "#34495e"
        self.endpoint_ent.config(state="disabled" if state else "normal", disabledbackground=bg_color, bg=bg_color)

    def refresh_peer_list(self):
        self.peer_listbox.delete(0, "end")
        for name in sorted(self.data["peers"].keys()): self.peer_listbox.insert("end", name)

    def on_select_peer(self, event):
        idx = self.peer_listbox.curselection()
        if not idx: return
        name = self.peer_listbox.get(idx); p = self.data["peers"][name]
        self.current_peer_id = name; self.name_var.set(name)
        for key in ["vpn_ip", "dns", "pub_key", "priv_key", "endpoint"]: getattr(self, f"{key}_var").set(p.get(key, ""))
        self.is_dynamic_var.set(p.get("is_dynamic", False))
        for lb, k in [(self.local_net_ui, "local_networks"), (self.links_ui, "linked_peers")]:
            lb.delete(0, "end")
            for i in p.get(k, []): lb.insert("end", i)
        self.toggle_dynamic()

    def new_peer(self):
        self.current_peer_id = None; self.name_var.set("")
        for k in ["vpn_ip", "dns", "pub_key", "priv_key", "endpoint"]: getattr(self, f"{k}_var").set("")
        self.is_dynamic_var.set(False); self.toggle_dynamic()
        for lb in [self.local_net_ui, self.links_ui]: lb.delete(0, "end")

    def save_current(self):
        name = self.name_var.get().strip()
        if not name: return
        new_links = list(self.links_ui.get(0, "end"))
        self.data["peers"][name] = {
            "vpn_ip": self.vpn_ip_var.get().strip(), "dns": self.dns_var.get().strip(),
            "pub_key": self.pub_key_var.get().strip(), "priv_key": self.priv_key_var.get().strip(),
            "endpoint": self.endpoint_var.get().strip(), "is_dynamic": self.is_dynamic_var.get(),
            "local_networks": list(self.local_net_ui.get(0, "end")), "linked_peers": new_links
        }
        for friend in new_links:
            if friend in self.data["peers"] and name not in self.data["peers"][friend]["linked_peers"]:
                self.data["peers"][friend]["linked_peers"].append(name)
        for other_name, other_data in self.data["peers"].items():
            if other_name != name and name in other_data["linked_peers"] and other_name not in new_links:
                other_data["linked_peers"].remove(name)
        self.save_data(); self.refresh_peer_list(); messagebox.showinfo("Saved", f"'{name}' updated.")

    def delete_peer(self):
        name = self.name_var.get()
        if name in self.data["peers"] and messagebox.askyesno("Confirm", f"Delete {name}?"):
            del self.data["peers"][name]
            for p in self.data["peers"].values():
                if name in p.get("linked_peers", []): p["linked_peers"].remove(name)
            self.save_data(); self.refresh_peer_list(); self.new_peer()

    def build_config_text(self):
        if not self.current_peer_id: return None
        me = self.data["peers"][self.current_peer_id]
        conf = f"[Interface]\nPrivateKey = {me.get('priv_key')}\nAddress = {me.get('vpn_ip')}\n"
        
        if me.get('dns'): conf += f"DNS = {me.get('dns')}\n"
        if not me.get('is_dynamic') and ":" in me.get('endpoint', ''):
            conf += f"ListenPort = {me['endpoint'].split(':')[-1]}\n"
        conf += "\n"

        for f_name in me.get("linked_peers", []):
            if f_name not in self.data["peers"]: continue
            f = self.data["peers"][f_name]
            
            # --- THE FIX ---
            # Extract only the IP address from the peer's VPN IP (removing /24, /28, etc.)
            peer_vpn_ip = f.get("vpn_ip", "").split('/')[0]
            # Re-attach /32 for a single host
            peer_host_route = f"{peer_vpn_ip}/32" if peer_vpn_ip else ""
            
            # Combine the single host route with their specific local networks
            allowed_list = [peer_host_route] + f.get("local_networks", [])
            # Filter out empty strings and join
            allowed_ips = ", ".join([x for x in allowed_list if x])
            
            conf += f"# Peer: {f_name}\n[Peer]\nPublicKey = {f.get('pub_key')}\n"
            if not f.get("is_dynamic") and f.get("endpoint"):
                conf += f"Endpoint = {f.get('endpoint')}\nPersistentKeepalive = 25\n"
            conf += f"AllowedIPs = {allowed_ips}\n\n"
        return conf

    def save_conf_to_file(self, content):
        filename = f"{self.current_peer_id}.conf"
        file_path = filedialog.asksaveasfilename(defaultextension=".conf", initialfile=filename, filetypes=[("WireGuard Config", "*.conf"), ("Text File", "*.txt")])
        if file_path:
            with open(file_path, "w") as f: f.write(content)
            messagebox.showinfo("Success", f"Saved to {file_path}")

    def export_config(self):
        conf = self.build_config_text()
        if not conf: return
        top = tk.Toplevel(self.root, bg="#1a252f")
        top.title(f"{self.current_peer_id}.conf")
        t = tk.Text(top, font=("Consolas", 11), bg="#2c3e50", fg="white", borderwidth=0, padx=10, pady=10)
        t.insert("1.0", conf); t.pack(fill="both", expand=True)
        btn_f = tk.Frame(top, bg="#1a252f", pady=10)
        btn_f.pack(fill="x")
        tk.Button(btn_f, text="SAVE TO FILE", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), relief="flat", padx=20, command=lambda: self.save_conf_to_file(conf)).pack()

    def export_qr(self):
        conf = self.build_config_text()
        if not conf: return
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(conf); qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_win = tk.Toplevel(self.root, bg="white")
        photo = ImageTk.PhotoImage(img); lbl = tk.Label(qr_win, image=photo, bg="white")
        lbl.image = photo; lbl.pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk(); app = WGWarden(root); root.mainloop()
