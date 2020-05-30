#!/usr/bin/env python3

import subprocess #Lets us issue shell commands.
import optparse #Lets the script take arguments.
import re #Regex
import sys #Let's us exit the script.

def get_arguments():
    #Create OptionParser object to handle arguments.
    parser = optparse.OptionParser()

    #Set up handling for interface argument.
    parser.add_option("-i", "--interface",
                     dest="arg_interface", #This is the dictionary key for the associated value.
                     help="Target interface for changing MAC address. e.g. -i eth0")

    #Set up handling for MAC address argument.
    parser.add_option("-m", "--mac",
                     dest="arg_new_mac", #This is the dictionary key for the associated value.
                     help="The new MAC address you want to use. e.g. -m 00:11:22:33:44:55")

    #Unpack the parse_args values into variables.
    (options, arguments) = parser.parse_args()

    #Check that both necessary arguments were provided and that they are valid.
    if not (options.arg_interface):
        #handle empty interface option
        parser.error("[-] Please provide a valid interface. Use --help for more info.")
    elif not (options.arg_new_mac):
        #handle empty new_mac option
        parser.error("[-] Please provide a valid MAC address. Use --help for more info.")
    else:
        #Return the options dictionary.
        return options


def change_mac(interface, new_mac):
    #Take down the target interface.
    print("[+] Turning off interface...")
    subprocess.run(["ifconfig", interface, "down"])

    #Reasign MAC address on target interface.
    print("[+] Re-assigning new MAC address {} for interface {}...".format(new_mac, interface))
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])

    #Bring the target interface back up.
    print("[+] Turning on interface...")
    subprocess.run(["ifconfig", interface, "up"])


def get_mac(interface):
    #Capture output of ifconfig, and save the MAC address in a variable.
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if (ifconfig_mac):
        #We only want the 1st match of our regex expression.
        return ifconfig_mac.group(0)
    else:
        print("[-] Could not read MAC address for target interface. Can this interface have a MAC address?") 
        sys.exit() #Exit the script.


#Get the options provided via arguments when script was run.
options = get_arguments()

#Check what the current MAC address is. NOTE: We have not made any changes yet.
current_mac = get_mac(options.arg_interface)
print("[+] The current MAC Address is: {}".format(current_mac))

#Change the MAC address using the options we got.
change_mac(options.arg_interface, options.arg_new_mac)

#Check what the current MAC address is AFTER having made changes via change_mac().
current_mac = get_mac(options.arg_interface)
if (current_mac == options.arg_new_mac):
    print("[+] SUCCESS! New MAC address for {}: {}".format(options.arg_interface, current_mac))
else:
    print("[-] Changing failed. Check input, and make sure target interface can have a MAC address.")
