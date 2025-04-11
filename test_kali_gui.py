import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch
import sys
import os

# Import your application module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kali_linux_gui import KaliToolsGUI  # Adjust import based on your actual file name

class TestKaliToolsGUI(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test"""
        self.root = tk.Tk()
        self.app = KaliToolsGUI(self.root)
    
    def tearDown(self):
        """Clean up after each test"""
        self.root.destroy()
    
    def test_initialization(self):
        """Test that the GUI initializes correctly"""
        self.assertEqual(self.root.title(), "Kali Linux Tools GUI")
        self.assertIsNotNone(self.app.notebook)
        self.assertIsNotNone(self.app.nmap_frame)
    
    def test_update_command(self):
        """Test command building functionality"""
        # Set up test values
        self.app.target_entry.insert(0, "192.168.1.1")
        self.app.port_entry.insert(0, "80,443")
        self.app.scan_type.set("-sS")
        self.app.timing_level.set(4)
        self.app.default_scripts.set(True)
        self.app.os_detection.set(True)
        
        # Update command
        self.app.update_command()
        
        # Check command contains expected elements
        command = self.app.command_preview.get()
        self.assertIn("-sS", command)
        self.assertIn("-p 80,443", command)
        self.assertIn("-T4", command)
        self.assertIn("-sC", command)
        self.assertIn("-O", command)
        self.assertIn("192.168.1.1", command)
    
    def test_run_nmap_without_target(self):
        """Test that running nmap without a target shows an error"""
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.app.run_nmap()
            mock_error.assert_called_once()
    
    @patch('subprocess.Popen')
    def test_run_nmap_with_target(self, mock_popen):
        """Test running nmap with a valid target"""
        # Mock process output
        mock_process = MagicMock()
        mock_process.stdout.readline.side_effect = ["Scanning host...", ""]
        mock_process.communicate.return_value = ("Scan complete", "")
        mock_popen.return_value = mock_process
        
        # Set a target and run
        self.app.target_entry.insert(0, "192.168.1.1")
        
        # Execute
        self.app.run_nmap()
        
        # Check results
        self.assertTrue(mock_popen.called)
        
        # Let the thread finish
        import time
        time.sleep(0.1)
    
    def test_timing_descriptions(self):
        """Test timing level descriptions"""
        descriptions = [self.app.get_timing_description(i) for i in range(6)]
        self.assertEqual(len(descriptions), 6)
        self.assertIn("Paranoid", descriptions[0])
        self.assertIn("Insane", descriptions[5])
    
    def test_clear_results(self):
        """Test clearing results"""
        # First add some text
        self.app.results_text.config(state=tk.NORMAL)
        self.app.results_text.insert(tk.END, "Test results")
        
        # Then clear it
        self.app.clear_results()
        
        # Check it's cleared
        self.assertEqual(self.app.results_text.get(1.0, tk.END).strip(), "")


class TestCommandBuilding(unittest.TestCase):
    """Focused tests for command building logic"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = KaliToolsGUI(self.root)
    
    def tearDown(self):
        self.root.destroy()
    
    def test_script_options(self):
        """Test script options are correctly added to command"""
        # Test default scripts
        self.app.default_scripts.set(True)
        self.app.update_command()
        self.assertIn("-sC", self.app.command_preview.get())
        
        # Test custom scripts
        self.app.script_entry.insert(0, "vuln,exploit")
        self.app.update_command()
        self.assertIn("--script=vuln,exploit", self.app.command_preview.get())
    
    def test_advanced_options(self):
        """Test advanced options are correctly added"""
        self.app.os_detection.set(True)
        self.app.aggressive_scan.set(True)
        self.app.verbose.set(True)
        self.app.update_command()
        
        command = self.app.command_preview.get()
        self.assertIn("-O", command)
        self.assertIn("-A", command)
        self.assertIn("-v", command)
    
    def test_additional_parameters(self):
        """Test additional parameters are correctly added"""
        self.app.additional_entry.insert(0, "--max-retries 2")
        self.app.update_command()
        self.assertIn("--max-retries 2", self.app.command_preview.get())


class TestCommandExecution(unittest.TestCase):
    """Tests for command execution functionality"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = KaliToolsGUI(self.root)
        
    def tearDown(self):
        self.root.destroy()
    
    @patch('subprocess.Popen')
    def test_execute_command_success(self, mock_popen):
        """Test successful command execution"""
        # Setup mock
        mock_process = MagicMock()
        mock_process.stdout.readline.side_effect = ["Line 1", "Line 2", ""]
        mock_process.communicate.return_value = ("", "")
        mock_popen.return_value = mock_process
        
        # Execute with mocked update_results to avoid GUI calls
        with patch.object(self.app, 'update_results') as mock_update:
            self.app.execute_command("nmap -sS 172.20.242.40")
            
            # Check results were updated
            self.assertEqual(mock_update.call_count, 4)  # 2 lines + "" + "Scan completed"
    
    @patch('subprocess.Popen')
    def test_execute_command_error(self, mock_popen):
        """Test command execution with error"""
        # Setup mock to raise exception
        mock_popen.side_effect = Exception("Command failed")
        
        # Execute with mocked update_results
        with patch.object(self.app, 'update_results') as mock_update:
            self.app.execute_command("invalid command")
            
            # Check error was reported
            mock_update.assert_called_with("Error executing command: Command failed")


if __name__ == '__main__':
    unittest.main()
