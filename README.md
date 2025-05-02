# CS499

CS499 Isaac and James Capstone Project

Documentation
______________________________________________________________________________________________
This script has only been tested on Kali Linux, so the steps may be different for other distros. 

# Installing and running the script:

Requirements: root access, git, python 3.11.8, nmap, and network connection

Steps:

Step 1: Navigate to the downloads folder using ``cd /home/(user)/Downloads/`` 

Step 2: Download the repository from the github using ``git clone https://github.com/James-dev-1/CS499`` with root privileges (either root shell or sudo)

Step 3: Optionally, move the downloaded folder to a working directory ex: ``mv /home/(user)/Downloads/CS499 /etc/CS499`` with root privileges

Step 4: Grant executable permissions to the script or directory with ``chmod +x /etc/CS499/cronjob-kali-gui.py`` with root privileges

Step 5: Run the python script with ``python3 /etc/CS499/cronjob-kali-gui.py`` with root privileges

________________________________________________________________________________________________
# Using the script:

Once the script is run, a gui will be opened. There are multiple tabs in the gui for the different features of the tool. The default tab is nmap, where commands can be created using input fields and buttons and run from the tool, showing the result in the console. There is also a tab for cronjobs with input fields to create custom cronjobs using the tool. Finally, there is a tab for uploading scripts that can be run with nmap against a target ip. 

________________________________________________________________________________________________
# Roadmap

In the future, features such as a dos tool tab, password sprayer tool tab, and brute force password tool tab are planned. 
_________________________________________________________________________________________________
# Disclaimer

This script was designed to be run in a virtual environment for educational purposes only. Do not use this tool on any networks without authorization from the network owner. Do not use this tool for malicious purposes. 
