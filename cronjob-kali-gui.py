import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import os
import re
from datetime import datetime

class KaliToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kali Linux Tools GUI")
        self.root.geometry("1000x800")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create nmap tab
        self.nmap_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.nmap_frame, text="Nmap")
        self.setup_nmap_tab()
        
        # Create cronjob tab
        self.cronjob_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cronjob_frame, text="Cronjob Manager")
        self.setup_cronjob_tab()
        
        # Create script upload tab
        self.script_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.script_frame, text="Script Upload")
        self.setup_script_upload_tab()
    
    def setup_script_upload_tab(self):
        # Script Upload Section
        upload_frame = ttk.LabelFrame(self.script_frame, text="Upload Custom Scripts")
        upload_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Destination directory selection
        ttk.Label(upload_frame, text="Destination Directory:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.script_dest_var = tk.StringVar(value="/usr/share/nmap/scripts/")
        dest_entry = ttk.Entry(upload_frame, textvariable=self.script_dest_var, width=50)
        dest_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # File selection button
        def select_script_file():
            filename = filedialog.askopenfilename(
                title="Select Nmap Script",
                filetypes=[("Nmap Scripts", "*.nse"), ("All files", "*.*")]
            )
            if filename:
                self.upload_script(filename)
        
        select_button = ttk.Button(upload_frame, text="Select Script", command=select_script_file)
        select_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Script list and management
        self.script_list_frame = ttk.LabelFrame(self.script_frame, text="Uploaded Scripts")
        self.script_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.script_listbox = tk.Listbox(self.script_list_frame, width=80)
        self.script_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar for script list
        scrollbar = ttk.Scrollbar(self.script_list_frame, orient=tk.VERTICAL, command=self.script_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.script_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons for script management
        button_frame = ttk.Frame(self.script_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        refresh_button = ttk.Button(button_frame, text="Refresh List", command=self.refresh_script_list)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_script)
        delete_button.pack(side=tk.LEFT, padx=5)
        
        # Initial script list refresh
        self.refresh_script_list()
    
    def upload_script(self, source_path):
        try:
            # Ensure destination directory exists and is writable
            dest_dir = self.script_dest_var.get()
            if not os.path.exists(dest_dir):
                messagebox.showerror("Error", f"Destination directory {dest_dir} does not exist.")
                return
            
            # Check if running with sudo
            if os.geteuid() != 0:
                messagebox.showerror("Error", "Script upload requires sudo privileges. Please run the application with sudo.")
                return
            
            # Copy script to destination
            filename = os.path.basename(source_path)
            dest_path = os.path.join(dest_dir, filename)
            
            # Use subprocess to copy with sudo
            subprocess.run(['sudo', 'cp', source_path, dest_path], check=True)
            
            # Set correct permissions
            subprocess.run(['sudo', 'chmod', '644', dest_path], check=True)
            
            messagebox.showinfo("Success", f"Script {filename} uploaded successfully to {dest_dir}")
            
            # Refresh script list
            self.refresh_script_list()
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to upload script: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def refresh_script_list(self):
        try:
            # Clear existing list
            self.script_listbox.delete(0, tk.END)
            
            # Get list of .nse scripts in the destination directory
            script_dir = self.script_dest_var.get()
            scripts = subprocess.check_output(['ls', script_dir]).decode().strip().split('\n')
            nse_scripts = [script for script in scripts if script.endswith('.nse')]
            
            # Populate listbox
            for script in sorted(nse_scripts):
                self.script_listbox.insert(tk.END, script)
        
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to list scripts. Check directory permissions.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def delete_selected_script(self):
        try:
            # Get selected script
            selection = self.script_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "No script selected.")
                return
            
            script = self.script_listbox.get(selection[0])
            script_path = os.path.join(self.script_dest_var.get(), script)
            
            # Confirm deletion
            confirm = messagebox.askyesno("Confirm", f"Delete script {script}?")
            if not confirm:
                return
            
            # Delete script with sudo
            subprocess.run(['sudo', 'rm', script_path], check=True)
            
            # Refresh list
            self.refresh_script_list()
            
            messagebox.showinfo("Success", f"Script {script} deleted successfully.")
        
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to delete script. Check permissions.")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def setup_cronjob_tab(self):
        # Cronjob Creation Section
        cronjob_frame = ttk.LabelFrame(self.cronjob_frame, text="Create Cronjob")
        cronjob_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Nmap Command Entry
        ttk.Label(cronjob_frame, text="Nmap Command:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.cronjob_command_var = tk.StringVar()
        command_entry = ttk.Entry(cronjob_frame, textvariable=self.cronjob_command_var, width=60)
        command_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Frequency Selection
        ttk.Label(cronjob_frame, text="Frequency:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Predefined frequency options
        freq_frame = ttk.Frame(cronjob_frame)
        freq_frame.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.freq_var = tk.StringVar(value="custom")
        
        freq_options = [
            ("Every 5 Minutes", "*/5 * * * *"),
            ("Hourly", "0 * * * *"),
            ("Daily", "0 0 * * *"),
            ("Weekly", "0 0 * * 0"),
            ("Monthly", "0 0 1 * *"),
            ("Custom", "custom")
        ]
        
        for text, value in freq_options:
            rb = ttk.Radiobutton(freq_frame, text=text, variable=self.freq_var, value=value, 
                                  command=self.toggle_custom_frequency)
            rb.pack(side=tk.LEFT, padx=5)
        
        # Custom Frequency Entry
        self.custom_freq_frame = ttk.Frame(cronjob_frame)
        self.custom_freq_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(self.custom_freq_frame, text="Custom Cron Expression:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.custom_freq_entry = ttk.Entry(self.custom_freq_frame, width=30)
        self.custom_freq_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Initially hide custom frequency
        self.custom_freq_frame.grid_remove()
        
        # Output Options
        ttk.Label(cronjob_frame, text="Output File:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.output_var = tk.StringVar(value="/var/log/nmap_scans/scan_{date}.log")
        output_entry = ttk.Entry(cronjob_frame, textvariable=self.output_var, width=60)
        output_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Create Cronjob Button
        create_button = ttk.Button(cronjob_frame, text="Create Cronjob", command=self.create_cronjob)
        create_button.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Existing Cronjobs Section
        existing_frame = ttk.LabelFrame(self.cronjob_frame, text="Existing Cronjobs")
        existing_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.existing_cron_text = scrolledtext.ScrolledText(existing_frame, wrap=tk.WORD, height=10)
        self.existing_cron_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Refresh Cronjobs Button
        refresh_button = ttk.Button(existing_frame, text="Refresh Cronjobs", command=self.refresh_existing_cronjobs)
        refresh_button.pack(pady=5)
        
        # Refresh existing cronjobs on startup
        self.refresh_existing_cronjobs()
    
    def toggle_custom_frequency(self):
        if self.freq_var.get() == "custom":
            self.custom_freq_frame.grid()
        else:
            self.custom_freq_frame.grid_remove()
    
    def create_cronjob(self):
        try:
            # Get command and frequency
            command = self.cronjob_command_var.get()
            if not command:
                messagebox.showerror("Error", "Please enter a valid Nmap command.")
                return
            
            # Determine frequency
            if self.freq_var.get() == "custom":
                cron_expr = self.custom_freq_entry.get()
                if not cron_expr:
                    messagebox.showerror("Error", "Please enter a valid cron expression.")
                    return
            else:
                cron_expr = self.freq_var.get()
            
            # Prepare output file with date formatting
            output_file = self.output_var.get().format(date=datetime.now().strftime("%Y%m%d_%H%M%S"))
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_file)
            subprocess.run(['sudo', 'mkdir', '-p', output_dir], check=True)
            
            # Full command with output redirection
            full_command = f"{command} > {output_file} 2>&1"
            
            # Construct full crontab entry
            crontab_entry = f"{cron_expr} {full_command}"
            
            # Add to current user's crontab
            # Use subprocess to run crontab command
            process = subprocess.Popen(['crontab', '-l'], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, 
                                       universal_newlines=True)
            existing_crontab, _ = process.communicate()
            
            # Append new cronjob
            new_crontab = existing_crontab.strip() + "\n" + crontab_entry + "\n"
            
            # Write back to crontab
            process = subprocess.Popen(['crontab', '-'], 
                                       stdin=subprocess.PIPE, 
                                       universal_newlines=True)
            process.communicate(input=new_crontab)
            
            messagebox.showinfo("Success", f"Cronjob created:\n{crontab_entry}")
            
            # Refresh existing cronjobs view
            self.refresh_existing_cronjobs()
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to create cronjob: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
    
    def refresh_existing_cronjobs(self):
        try:
            # Clear existing text
            self.existing_cron_text.config(state=tk.NORMAL)
            self.existing_cron_text.delete(1.0, tk.END)
            
            # Retrieve current user's crontab
            process = subprocess.Popen(['crontab', '-l'], 
                                       stdout=subprocess.PIPE, 
                                       stderr=subprocess.PIPE, 
                                       universal_newlines=True)
            existing_crontab, _ = process.communicate()
            
            # Insert crontab contents
            self.existing_cron_text.insert(tk.END, existing_crontab)
            self.existing_cron_text.config(state=tk.DISABLED)
        
        except subprocess.CalledProcessError:
            # This can happen if no crontab exists
            self.existing_cron_text.insert(tk.END, "No existing cronjobs found.")
            self.existing_cron_text.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve cronjobs: {str(e)}")

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