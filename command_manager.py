#***********************************************************************************************************************#
#   --usage:                                                                                                            #
#             ./CommandsManager.py                                                                                      #
#         or  python CommandsManager.py                                                                                 #
#                                                                                                                       #
# date:  17/08/2025 Created                                                                                             #
#***********************************************************************************************************************#

##################
# Import Section #
##################

import time
import yaml
from requests.auth import HTTPBasicAuth
import threading
from paramiko import SSHClient, MissingHostKeyPolicy
from datetime import datetime

#############
# Variables #
#############

# List that will save all the commands required
Command_List = []

# Command List File Path 
Command_List_File_Path = "command_list.txt"

# Network configuration File Path
Network_Config_File_Path = "network_config.yaml"

#####################
# Functions Section #
#####################

# Function that clear the SSH buffer
def clear_buffer(connection, bufferSize):
    if connection.recv_ready():
        return connection.recv(bufferSize)

# Function that read all the commands requested from a file and will save then into a List
def read_Commands_File():

    # Auxilear List
    List = []

    # We open the file Command_List.txt with read privileagues
    with open(Command_List_File_Path, 'r') as file:
        for Line in file:
            List.append(Line)

    # Delete all posibles blank lines in the List variable
    List = ' '.join(List).split('\n')

    #Closing the Command_List.txt File
    file.close()

    #Returning the List with the commands
    return List

# Function that will return a yaml variable with all network config
def read_Network_Config():

    # Open the YAML file in read mode
    with open(Network_Config_File_Path, 'r') as file:
    
        # Load the YAML content from the file
        data = yaml.safe_load(file)

    return data

# Function that create the SSH session to the Host defined
def get_connection(Host, Credentials, SSH_Options):

    #We generate the SSH Client object
    ssh = SSHClient()

    try:
        #We check the system host keys for hosts
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(MissingHostKeyPolicy())

        #Generate the SSH connection with the credentials
        ssh.connect(hostname=Host, username=Credentials['username'], password=Credentials['password'], port=SSH_Options['NetworkDevice_SSH_Port'], allow_agent=SSH_Options['Allow_agent'], compress=SSH_Options['Compress'], look_for_keys=SSH_Options['Look_for_keys'])

    #Cauth the possible errors in the SSH Connection
    except ssh.AuthenticationException:
        print("Authentication failed, please verify your credentials: %s")
    except ssh.SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
    except ssh.BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)
    except Exception as e:
        print("Unable to Authenticate with remote Network Device")
        exit()

    #Return the SSH session
    return ssh

# Function to handle a single network device
# Bassically connect to a single device, execute the command and save the output into a file.
def process_device(device, network_Config, Command_List):

    # Date Class for the filename identification
    now = datetime.now()

    # Variable that generates the filename with the hostname and generation date
    NetworkDevice_FILENAME = (device).lower() + "-" + now.strftime("%Y-%m-%d-%H-%M-%S") + ".txt"

    # Open the file to write the cmd outputs
    try:
        NETDEV_CMD_OUTPUT = open(NetworkDevice_FILENAME, "x")
    except FileExistsError:
        NETDEV_CMD_OUTPUT = open(NetworkDevice_FILENAME, "w")

    # Generate the SSH Connection
    ssh = get_connection(device, network_Config['Credentials'], network_Config['SSH_Options'])

    # If there is not ssh connection we exit the function with no cmd result for this Network Device
    if not ssh:

        # Skip this device if the connection failed
        print(f"Failed to connect to {device}.")
        NETDEV_CMD_OUTPUT.close()
        return

    try:
        # Invoke a shell through the SSH Connection
        Shell = ssh.invoke_shell()

        # Disable terminal length to display the full output of commands
        Shell.send('terminal length 0\n')

        # Wait for the device to process the command
        time.sleep(1)

        # For each command in the list, send the command to the network device
        for cmd in Command_List:
            # Check if the Command is not empty and is not a blank space
            if cmd.strip():
                # Send the command with a newline character to execute it
                Shell.send(f'{cmd.strip()}\n')
                
                # Wait for the device to respond
                time.sleep(network_Config['SSH_Options']['Time_Sleep'])
                
                # Read the output from the device
                output = Shell.recv(network_Config['SSH_Options']['NetworkDeviceMaxBuffer']).decode('UTF-8')

                # Write the output to the file
                NETDEV_CMD_OUTPUT.write(output)
                NETDEV_CMD_OUTPUT.write("\n")
                NETDEV_CMD_OUTPUT.write("\n")

    finally:
        # Close the file after all commands have been executed
        NETDEV_CMD_OUTPUT.close()
        
        # Close the Shell Connection
        Shell.close()
        
        # Close the SSH Connection
        ssh.close()

# Main program that fecth the cmd output from network devices and save it inside a file
def main():

    # Read all the commands to be executed from File
    Command_List = read_Commands_File()

    # Read all Network Configuration options from File
    network_Config = read_Network_Config()

    # List of threaths
    threads = []

    # For each network device in the list, create a new thread
    for device in network_Config['NetworkDevice']:

        # Create a new thread with the process_device function as the target
        thread = threading.Thread(target=process_device, args=(device, network_Config, Command_List))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

################
# Main Program #
################

if __name__ == '__main__':
    exit(main())