# Kali Linux Network Tools Web Interface

## Prerequisites
- Apache2 Web Server
- PHP 7.4+
- Sudo Permissions
- Nmap Installed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kali-network-tools.git
cd kali-network-tools
```

2. Configure Apache:
```bash
sudo a2enmod php
sudo systemctl restart apache2
```

3. Set Permissions:
```bash
sudo chown -R www-data:www-data /path/to/nmap-web-tool
sudo chmod -R 755 /path/to/nmap-web-tool
```

4. Configure Sudo for Web User:
```bash
# Edit sudoers file
sudo visudo

# Add these lines to allow www-data to run nmap without password
www-data ALL=(ALL) NOPASSWD: /usr/bin/nmap
www-data ALL=(ALL) NOPASSWD: /bin/mv
www-data ALL=(ALL) NOPASSWD: /bin/chmod
```

## Security Considerations
- Limit access to the web interface
- Use SSL/TLS
- Implement strong authentication
- Regularly update dependencies

## Features
- Nmap Scan Configuration
- NSE Script Management
- Cronjob Scheduling
- Web-based Interface
```
