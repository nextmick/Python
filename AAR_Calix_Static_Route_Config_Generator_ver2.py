
#Future Improvements
#Add NetMiko to at least run the show commands for you.
#Add different VLANS
#Give it modules and arguments like Blue's Script
#
#
#

#import readline # - IMPORTANT.  THIS NEEDS TO BE ACTIVE IN THE LINUX SERVER
import sys
import datetime
import ipaddress
date = datetime.datetime.now()

SitesList = (
    "ALPN",     #0
    "CV1X",     #1
    "DT1X",     #2
    "ELCN",     #3
    "ESCN",     #4
    "FED1",     #5
    "OCNS",     #6
    "PWY1",     #7
    "VIST",     #8
    "ALSV",     #9
    "DNPT",     #10
    "IRVN",     #11
    "ORNG",     #12
    "PLSV",     #13
    "RSMT",     #14
    "SNTB",     #16
)


BadMaskList = (
    "255.255.255.255",
    "255.255.255.254",
)

BreakList = (
    "0.0.0.0",
)


username = input("Enter your Username: ")


SiteMatch = False
Site = ""
while SiteMatch is False:
    Site = (input("Enter a CA Site in CAPS (ie ALSV): "))
    if Site in SitesList:
        SiteMatch = True
    else:
        print("Invalid Site")



all_good = False
ip_try = False
Mask_OK = False
ipblock = ()
NetMask = ()


while ip_try is False or all_good is False:
    try:
        ipblock = ipaddress.IPv4Network(input("Enter IP Block with Slash Notation: "))
        try:
            NetMask = str(ipblock.netmask)
            ip_try = True
        except: 
            print("Error.  Pizza.  Please try again.")
    except:
        print("Error.  You need to enter the NETWORK address with the slash notation.  Please try again (Enter 0.0.0.0/0 to Exit)" )
    if NetMask in BreakList:
        sys.exit()
    elif NetMask in BadMaskList:
        all_good = False
        print ("/31s and /32s are not allowed.  Please play again (Enter 0.0.0.0/0 to Exit.)")
    else:
        all_good = True



Network_Address = ipblock.network_address
AAR1Address = Network_Address + 2
AAR2Address = Network_Address + 3
VirtualAddress = Network_Address + 1
Slash = ipblock.prefixlen

def Show_Commands():
    if Site in SitesList:
        print(" ")
        print("!!!!!!!! SHOW COMMANDS !!!!!!!!")
        print("In " + str(Site) + "HUBC01:")
        print("show route " + str(AAR1Address))
        print("!EXPECTED OUTPUT: 0.0.0.0/0")
        print("show route longer " + str(Network_Address)+ "/23")
        print("!EXPECTED OUTPUT: NETWORK NOT LISTED")
        print(" ")
    else:
        print("Invalid Site")
        quit()
Show_Commands()


def Configs():
    print("!!!!!!!!!!!!!! " + Site + "AARA01 !!!!!!!!!!!!!!")
    print("configure session " + username + date.strftime("%b%d%Y"))
    print("interface vlan 200")
    print("ip address " + str(AAR1Address) + "/" + str(Slash) + " secondary")
    print("ip virtual-router address " + str(VirtualAddress))
    print("exit")
    print("ip prefix-list V4-CONNECTED-DATA-BUSINESS")
    print("permit " + ipblock.with_prefixlen)
    print("exit")
    print("show session diffs")
    print("!commit - MAKE SURE YOU'RE GOOD FIRST!")
    print(" ")
    print(" ")
    print("!!!!!!!!!!!!!! " + Site + "AARA02 !!!!!!!!!!!!!!")
    print("configure session " + username + date.strftime("%b%d%Y"))
    print("interface vlan 200")
    print("ip address " + str(AAR2Address) + "/" + str(Slash) + " secondary")
    print("ip virtual-router address " + str(VirtualAddress))
    print("exit")
    print("ip prefix-list V4-CONNECTED-DATA-BUSINESS")
    print("permit " + ipblock.with_prefixlen)
    print("exit")
    print("show session diffs")
    print("!commit - MAKE SURE YOU'RE GOOD FIRST!")
    print(" ")
    print(" ")
Configs()



#ARISTA CONFIG EXAMPLE:
#Block - 98.189.23.176/28
#
#
#In ALSVHUBC01:
#show route [ip address]
#show route longer [ip address]/23
#
#In FED1HUBC01:
#show route [ip address]
#show route longer [ip address]/23
#
#
#
#
#!!!!!!!!!!!!! RSMTAARA01 !!!!!!!!!!!!!
#configure session jasparkeJan282022
#interface vlan200
#ip address 98.189.23.178/28 secondary
#ip virtual-router address 98.189.23.177
#exit
#ip prefix-list V4-CONNECTED-DATA-BUSINESS
#permit 98.189.23.176/28
#exit
#show session diffs
#commit
#
#!!!!!!!!!!!!! RSMTAARA02 !!!!!!!!!!!!!
#configure session jasparkeJan282022
#interface vlan200
#ip address 98.189.23.179/28 secondary
#ip virtual-router address 98.189.23.177
#exit
#ip prefix-list V4-CONNECTED-DATA-BUSINESS
#permit 98.189.23.176/28
#exit
#show session diffs
#commit

	