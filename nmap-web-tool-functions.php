<?php
// Security: Prevent direct file access
if (!defined('SECURE_INCLUDE')) {
    die('No direct script access allowed');
}

/**
 * Build Nmap Command
 * Constructs a safe and configurable Nmap command
 */
function build_nmap_command($target, $scan_type, $ports, $scripts, $timing, $additional_options = []) {
    // Sanitize inputs
    $target = escapeshellarg($target);
    $scan_type = escapeshellarg($scan_type);
    $timing = escapeshellarg($timing);

    // Base command
    $command = "sudo nmap {$scan_type} -T{$timing}";

    // Add ports if specified
    if (!empty($ports)) {
        $sanitized_ports = escapeshellarg($ports);
        $command .= " -p {$sanitized_ports}";
    }

    // Add NSE scripts if specified
    if (!empty($scripts)) {
        $sanitized_scripts = escapeshellarg($scripts);
        $command .= " --script={$sanitized_scripts}";
    }

    // Add additional options
    foreach ($additional_options as $option) {
        $command .= " " . escapeshellarg($option);
    }

    // Append target
    $command .= " {$target}";

    return $command;
}

/**
 * Execute Nmap Scan
 * Runs the nmap command and returns results
 */
function execute_nmap_scan($command) {
    // Log the command for audit purposes
    error_log("Executing Nmap Scan: {$command}");

    // Execute command and capture output
    $output = [];
    $return_var = 0;
    exec($command, $output, $return_var);

    // Check for execution errors
    if ($return_var !== 0) {
        return "Error executing scan. Check command and permissions.";
    }

    return implode("\n", $output);
}

/**
 * List NSE Scripts
 * Retrieves available NSE scripts
 */
function list_nse_scripts() {
    $script_dir = '/usr/share/nmap/scripts/';
    $scripts = glob($script_dir . '*.nse');
    return array_map('basename', $scripts);
}

/**
 * Upload NSE Script
 * Handles script upload with permission checks
 */
function upload_nse_script($tmp_name, $filename) {
    $upload_dir = '/usr/share/nmap/scripts/';
    $destination = $upload_dir . basename($filename);

    // Validate file type
    $file_extension = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
    if ($file_extension !== 'nse') {
        return false;
    }

    // Use sudo to move file and set permissions
    $command = "sudo mv " . escapeshellarg($tmp_name) . " " . escapeshellarg($destination) . 
               " && sudo chmod 644 " . escapeshellarg($destination);
    
    exec($command, $output, $return_var);
    return $return_var === 0;
}

/**
 * Create Cronjob
 * Adds a new cronjob for scheduled scans
 */
function create_cronjob($command, $schedule) {
    // Sanitize inputs
    $sanitized_command = escapeshellarg($command);
    $sanitized_schedule = escapeshellarg($schedule);

    // Construct crontab entry
    $crontab_entry = "{$sanitized_schedule} {$sanitized_command}";

    // Add to current user's crontab
    exec("(crontab -l 2>/dev/null; echo {$crontab_entry}) | crontab -", $output, $return_var);

    return $return_var === 0;
}

/**
 * List Cronjobs
 * Retrieves current user's cronjobs
 */
function list_cronjobs() {
    exec("crontab -l", $output, $return_var);
    return $return_var === 0 ? $output : [];
}
