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


