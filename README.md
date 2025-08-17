<img src="images/af806e83-9735-4f5a-828a-89960ec5eeee.jpg" alt="Alt Text" width="500"/>

![Alt Text](images/af806e83-9735-4f5a-828a-89960ec5eeee.jpg)

# Network-Troubleshooting-Toolkit

This project is a Python-based Network Troubleshooting Toolkit designed to automate the collection of diagnostic information from multiple network devices simultaneously. It connects to a list of network devices, executes a predefined list of "show" commands, and saves the output to individual, timestamped text files. This tool is specifically built for network troubleshooting and gathering diagnostic data and does not perform any configuration changes on the network devices.

# Features

* Multi-threaded Execution: The script uses threading to connect to and collect data from multiple network devices concurrently, significantly reducing the time required for data collection.

* Secure SSH Connectivity: It leverages the Paramiko library to establish secure SSH connections.

* Customizable: The list of commands to be executed and the network devices to be queried are read from separate files (`Command_List.txt` and `network_config.yaml`), allowing for easy customization without modifying the core script.

* Automated Data Collection: It automates the execution of commands like `show version`, `show hardware`, and `show ip int brief` to gather critical troubleshooting data.

* Organized Output: The output from each network device is saved to a unique text file, with the filename automatically generated to include the device hostname and a timestamp for easy identification and review.

# Getting Started

## Prerequisites

* Python 3.x
* The paramiko library (`pip install paramiko`)
* The pyyaml library (`pip install pyyaml`)

## Installation

1. Clone the repository:

```bash
  git clone https://github.com/your-username/Network-Troubleshooting-Toolkit.git
  cd Network-Troubleshooting-Toolkit
```
2. Install the required Python libraries.

  ```bash
    pip install paramiko pyyaml
  ```
# Usage

1. Configure Network Devices and Credentials:

    Edit the `network_config.yaml` file to add your network device hostnames or IP addresses, along with the SSH credentials and connection options.

```yaml
  # Authentication variables for SSH
  Credentials:
      username : "your_username"
      password : "your_password"

  # SSH connection options available for the SSH connection
  SSH_Options:
      NetworkDevice_SSH_Port : 22
      NetworkDeviceMaxBuffer : 65535
      Time_Sleep : 20
      Allow_agent: True
      Compress: True
      Look_for_keys: False

  # Network Device FQDN or IP Address
  NetworkDevice:
      - router.1.fqdn
      - 1.2.3.4
```

2. Define Commands:

    Edit the `Command_List.txt` file and enter the "show" commands you want to execute, with one command per line.

    ```bash
        show version
        show hardware
        show module
        show inventory
        show ip int brief
    ```

3. Run the Script:

   Execute the `command_manager.py` script from your terminal:

   ```bash
     python command_manager.py
   ```

   or

   ```bash
    chmod +x command_manager.py
    ./command_manager.py
   ```

4. Review Output:

   The script will create .txt files in the same directory, each named after the network device and a timestamp (e.g., `router.1.fqdn-2025-08-17-18-00-00.txt)`. These files contain the output of the executed commands.

# Disclaimer

This tool is provided "as is" and is intended for informational and troubleshooting purposes only. The user assumes all responsibility for its use. The script is designed to only run "show" commands and is not intended for making configuration changes. Any modifications to the script to perform configuration changes are at the user's own risk.
