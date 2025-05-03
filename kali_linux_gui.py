# Kali Linux Python Tool Version 2
# Created by James and Isaac for CS499 Project
# Fix major bugs from Version 1 and add script uploader and placeholder tab for future tools
# Future plans include Cronjob
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import re

class KaliToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kali Linux Tools GUI")
        self.root.geometry("900x700")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create nmap tab
        self.nmap_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.nmap_frame, text="Nmap")
        self.setup_nmap_tab()
        
        # Placeholder for additional tools
        # self.create_placeholder_tab("Metasploit")
        # self.create_placeholder_tab("Aircrack-ng")
        # self.create_placeholder_tab("Hydra")
    
    def setup_nmap_tab(self):
        # Target section
        target_frame = ttk.LabelFrame(self.nmap_frame, text="Target Specification")
        target_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(target_frame, text="Target IP/Host/Range:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.target_entry = ttk.Entry(target_frame, width=50)
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Scan type section
        scan_frame = ttk.LabelFrame(self.nmap_frame, text="Scan Type")
        scan_frame.pack(fill=tk.X, padx=10, pady=5)
        # Options for nmap scan type 
        self.scan_type = tk.StringVar(value="-sS")
        ttk.Radiobutton(scan_frame, text="TCP SYN Scan (-sS)", variable=self.scan_type, value="-sS").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Radiobutton(scan_frame, text="TCP Connect Scan (-sT)", variable=self.scan_type, value="-sT").grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        ttk.Radiobutton(scan_frame, text="UDP Scan (-sU)", variable=self.scan_type, value="-sU").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Radiobutton(scan_frame, text="FIN Scan (-sF)", variable=self.scan_type, value="-sF").grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        ttk.Radiobutton(scan_frame, text="Ping Scan (-sn)", variable=self.scan_type, value="-sn").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        ttk.Radiobutton(scan_frame, text="Version Detection (-sV)", variable=self.scan_type, value="-sV").grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Port specification section
        port_frame = ttk.LabelFrame(self.nmap_frame, text="Port Specification")
        port_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(port_frame, text="Port Range:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.port_entry = ttk.Entry(port_frame, width=30)
        self.port_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(port_frame, text="Examples: 22; 1-1000; 80,443,8080").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Script section
        script_frame = ttk.LabelFrame(self.nmap_frame, text="NSE Scripts")
        script_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.default_scripts = tk.BooleanVar()
        ttk.Checkbutton(script_frame, text="Default Scripts (-sC)", variable=self.default_scripts).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(script_frame, text="Custom Scripts:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.script_entry = ttk.Entry(script_frame, width=50)
        self.script_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Label(script_frame, text="(e.g., vuln,exploit)").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Timing and performance section
        timing_frame = ttk.LabelFrame(self.nmap_frame, text="Timing and Performance")
        timing_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.timing_level = tk.IntVar(value=3)
        for i in range(6):
            ttk.Radiobutton(timing_frame, text=f"T{i} - {self.get_timing_description(i)}", 
                         variable=self.timing_level, value=i).grid(row=i//3, column=i%3, padx=5, pady=2, sticky=tk.W)
        
        # Advanced options section
        adv_frame = ttk.LabelFrame(self.nmap_frame, text="Advanced Options")
        adv_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.os_detection = tk.BooleanVar()
        ttk.Checkbutton(adv_frame, text="OS Detection (-O)", variable=self.os_detection).grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        
        self.aggressive_scan = tk.BooleanVar()
        ttk.Checkbutton(adv_frame, text="Aggressive Scan (-A)", variable=self.aggressive_scan).grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        
        self.verbose = tk.BooleanVar()
        ttk.Checkbutton(adv_frame, text="Verbose (-v)", variable=self.verbose).grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        
        # Additional options section
        additional_frame = ttk.LabelFrame(self.nmap_frame, text="Additional Options")
        additional_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(additional_frame, text="Additional Parameters:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.additional_entry = ttk.Entry(additional_frame, width=50)
        self.additional_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Command preview
        preview_frame = ttk.LabelFrame(self.nmap_frame, text="Command Preview")
        preview_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.command_preview = ttk.Entry(preview_frame, width=100)
        self.command_preview.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W+tk.E)
        
        preview_button = ttk.Button(preview_frame, text="Update Command", command=self.update_command)
        preview_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Buttons section
        button_frame = ttk.Frame(self.nmap_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        run_button = ttk.Button(button_frame, text="Run Scan", command=self.run_nmap)
        run_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(button_frame, text="Clear Results", command=self.clear_results)
        clear_button.pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(self.nmap_frame, text="Scan Results")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_text.config(state=tk.DISABLED)
        
        # Initialize command preview
        self.update_command()
    
    def get_timing_description(self, level):
        descriptions = [
            "Paranoid (very slow)",
            "Sneaky (slow)",
            "Polite (normal)",
            "Normal (default)",
            "Aggressive (fast)",
            "Insane (very fast)"
        ]
        return descriptions[level]
    
    def create_placeholder_tab(self, name):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name)
        
        message = f"The {name} interface will be implemented here."
        label = ttk.Label(frame, text=message)
        label.pack(padx=20, pady=20)
    
    def update_command(self):
        # Build the nmap command based on the selected options
        command = "nmap "
        
        # Add scan type
        command += f"{self.scan_type.get()} "
        
        # Add ports if specified
        if self.port_entry.get().strip():
            command += f"-p {self.port_entry.get().strip()} "
        
        # Add timing
        command += f"-T{self.timing_level.get()} "
        
        # Add scripts
        if self.default_scripts.get():
            command += "-sC "
        if self.script_entry.get().strip():
            command += f"--script={self.script_entry.get().strip()} "
        
        # Add advanced options
        if self.os_detection.get():
            command += "-O "
        if self.aggressive_scan.get():
            command += "-A "
        if self.verbose.get():
            command += "-v "
        
        # Add additional parameters
        if self.additional_entry.get().strip():
            command += f"{self.additional_entry.get().strip()} "
        
        # Add target (last parameter)
        if self.target_entry.get().strip():
            command += self.target_entry.get().strip()
        else:
            command += "<target>"
        
        # Update the command preview
        self.command_preview.delete(0, tk.END)
        self.command_preview.insert(0, command)
    
    def run_nmap(self):
        # Check if target is specified
        if not self.target_entry.get().strip():
            messagebox.showerror("Error", "Please specify a target IP, hostname, or range.")
            return
        
        # Update the command to ensure it's current
        self.update_command()
        
        # Get the command from the preview
        command = self.command_preview.get()
        
        # Enable the results text widget and clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Running command: {command}\n\n")
        self.results_text.config(state=tk.DISABLED)
        self.root.update()
        
        # Run nmap in a separate thread to avoid freezing the GUI
        threading.Thread(target=self.execute_command, args=(command,), daemon=True).start()
    
    def execute_command(self, command):
        try:
            # Parse the command into arguments
            args = []
            in_quotes = False
            current_arg = ""
            
            for char in command:
                if char == ' ' and not in_quotes:
                    if current_arg:
                        args.append(current_arg)
                        current_arg = ""
                elif char == '"':
                    in_quotes = not in_quotes
                else:
                    current_arg += char
            
            if current_arg:
                args.append(current_arg)
            
            # Execute the command
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
            
            # Process output in real-time
            for line in iter(process.stdout.readline, ''):
                self.update_results(line)
            
            # Get any remaining output
            stdout, stderr = process.communicate()
            
            if stdout:
                self.update_results(stdout)
            
            if stderr:
                self.update_results(f"Error: {stderr}")
            
            self.update_results("\nScan completed.")
        
        except Exception as e:
            self.update_results(f"Error executing command: {str(e)}")
    
    def update_results(self, text):
        # Update the results text widget from the main thread
        self.root.after(0, self._update_results, text)
    
    def _update_results(self, text):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, text)
        self.results_text.see(tk.END)
        self.results_text.config(state=tk.DISABLED)
    
    def clear_results(self):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = KaliToolsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
