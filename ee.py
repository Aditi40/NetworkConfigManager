import subprocess
import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext


class NetworkConfigManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Configuration Manager")
        
        self.output_area = scrolledtext.ScrolledText(root, width=80, height=20)
        self.output_area.pack(pady=10)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ("Display Interfaces", self.display_interfaces),
            ("View Configuration", self.view_configuration),
            ("Set Static IP", self.set_static_ip),
            ("Disable DHCP", self.disable_dhcp),
            ("Set DHCP", self.set_dhcp),
            ("Change DNS", self.change_dns),
            ("Ping Test", self.ping_test),
            ("Save Configuration", self.save_configuration),
            ("Load Configuration", self.load_configuration),
            ("Reset Network Settings", self.reset_network_settings),
            ("Exit", self.root.quit)
        ]
        
        for (text, command) in buttons:
            btn = tk.Button(self.root, text=text, command=command)
            btn.pack(pady=5)
    def disable_dhcp(self):
        interface = simpledialog.askstring("Input", "Enter interface name:")
        ip = simpledialog.askstring("Input", "Enter static IP:")
        subnet = simpledialog.askstring("Input", "Enter subnet mask:")
        gateway = simpledialog.askstring("Input", "Enter gateway:")

        if interface and ip and subnet and gateway:
            try:

                subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', interface, 'static', ip, subnet, gateway], check=True)
                messagebox.showinfo("Success", f"Disabled DHCP on {interface} and set static IP {ip}/{subnet} with gateway {gateway}.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to set static IP: {e}")

    def reset_network_settings(self):
        interface = simpledialog.askstring("Input", "Enter interface name:")
        if interface:
            try:

                subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', interface, 'dhcp'], check=True)

                subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', interface, 'dhcp'], check=True)
                messagebox.showinfo("Success", f"Reset settings for {interface} to DHCP.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to reset network settings: {e}")



    def display_interfaces(self):
        interfaces = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, interfaces.stdout)

    def view_configuration(self):
        interface = simpledialog.askstring("Input", "Enter interface name:")
        if interface:
            result = subprocess.run(['netsh', 'interface', 'ip', 'show', 'config', interface], capture_output=True, text=True)
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, result.stdout)

    def set_static_ip(self):
        interface = simpledialog.askstring("Input", "Enter interface name:")
        ip = simpledialog.askstring("Input", "Enter static IP:")
        subnet = simpledialog.askstring("Input", "Enter subnet mask:")
        gateway = simpledialog.askstring("Input", "Enter gateway:")
        if interface and ip and subnet and gateway:
            try:
                subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', interface, 'static', ip, subnet, gateway], check=True)
                messagebox.showinfo("Success", f"Set static IP {ip}/{subnet} on {interface} with gateway {gateway}.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to set static IP: {e}")

    def set_dhcp(self):
        interface = simpledialog.askstring("Input", "Enter interface name:")
        if interface:
            try:
                subprocess.run(['netsh', 'interface', 'ip', 'set', 'address', interface, 'dhcp'], check=True)
                messagebox.showinfo("Success", f"DHCP enabled on {interface}.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to enable DHCP: {e}")

    def change_dns(self):
        interface = simpledialog.askstring("Input", "Enter interface name:")
        dns_servers = simpledialog.askstring("Input", "Enter DNS servers (comma-separated):")
        if interface and dns_servers:
            dns_list = [dns.strip() for dns in dns_servers.split(',')]
            try:
                for dns in dns_list:
                    subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', interface, 'static', dns], check=True)
                messagebox.showinfo("Success", "DNS servers updated.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to change DNS: {e}")

    def ping_test(self):
        host = simpledialog.askstring("Input", "Enter host to ping:")
        if host:
            response = os.system(f"ping {host} -n 4")
            result = f"{host} is reachable." if response == 0 else f"{host} is not reachable."
            self.output_area.delete(1.0, tk.END)
            self.output_area.insert(tk.END, result)

    def save_configuration(self):
        filename = simpledialog.askstring("Input", "Enter filename to save configuration:")
        if filename:
            config = {}
            interfaces = subprocess.run(['netsh', 'interface', 'show', 'interface'], capture_output=True, text=True)
            config['interfaces'] = interfaces.stdout
            with open(filename, 'w') as f:
                json.dump(config, f)
            messagebox.showinfo("Success", f"Configuration saved to {filename}.")

    def load_configuration(self):
        filename = simpledialog.askstring("Input", "Enter filename to load configuration:")
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                    self.output_area.delete(1.0, tk.END)
                    self.output_area.insert(tk.END, config['interfaces'])
            except FileNotFoundError:
                messagebox.showerror("Error", "Configuration file not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkConfigManager(root)
    root.mainloop()
