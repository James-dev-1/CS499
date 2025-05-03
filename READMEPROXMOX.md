# ProxMox VE for practice
This document will describe the environment we used our python attack scripts within. This environment is virtualized and provides a network to practice threat defense and prevention.
____________________________________________________________________________
## Requirements
You must have a device running ProxMox that has the CPU, RAM, and storage capacity for multiple virtual machines. This is assuming Proxmox is already configured with a functional setup. Access to the management web page and permissions to create and manage vms and storage. 
____________________________________________________________________________
## Steps
Step 1: Download the necessary ISO files. For our environment, we used one virtual machine of each type: Centos7, Fedora21, Debian10, Ubuntu24, Kali 2025, and Palo Alto. An open source alternative to Palo Alto would be OPNsense.

Step 2: Access the management web page and authenticate as a user with the necessary privileges. 

Step 3: Navigate to the "Server View". Within the "Data Center" locate the server, "pve01" if default naming scheme is used, and click the drop down arrow. 

Step 4: At the bottom of the list of VMs, groups, and pools hosted onthe server, there will be the local storage of the node, "local(pve01)". pve01 is just a placeholder and should reflect your server name.

Step 5: Within the local storage, navigate to the "ISO Images" tab and click "Upload" to launch the upload wizard. 

Step 6: Upload each ISO file you downloaded earlier you wish to use with the tool.

Step 7: Next, create VMs using the "Create VM" button in the top right using each of the ISO files you downloaded.

Step 8: Once the VMs are installed, begin by configuring virtual networks for the VMs. Add a "Zone" in the "SDN" section of the "Data Center" followed by a "VNet" that uses the created zone. 

Step 9: On each VM, add an interface using the newly created VNet. On the router VM, add multiple interfaces using the newly created VNet and one interface using a VNet with external internet access.

Step 10: Once networking is configured, the environment is ready to be used. Set up simple services, install the python tool, and begin practicing detecting and defending nmap scans and scripted attacks. 
