<?php
// Security: Prevent direct file access
define('SECURE_INCLUDE', true);

// Application Configuration
$config = [
    'app_name' => 'Kali Linux Network Tools',
    'version' => '1.0.0',
    
    // Directories
    'script_upload_dir' => '/usr/share/nmap/scripts/',
    'scan_log_dir' => '/var/log/nmap_scans/',
    
    // Security Settings
    'allowed_script_extensions' => ['nse'],
    'max_upload_size' => 1024 * 1024, // 1MB
    
    // Logging
    'enable_logging' => true,
    'log_file' => '/var/log/nmap_web_tool.log'
];

// Error Reporting (Adjust based on environment)
error_reporting(E_ALL);
ini_set('display_errors', 1);
