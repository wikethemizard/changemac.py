#!/usr/bin/env python3

import subprocess #Lets us issue shell commands.
import optparse #Lets the script take arguments.

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

    print("[i] Done!")


#Change the mac using the options we got.
options = get_arguments()
change_mac(options.arg_interface, options.arg_new_mac)
