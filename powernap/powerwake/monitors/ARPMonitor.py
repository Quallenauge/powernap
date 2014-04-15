#
#    powernapd plugin - ARP Monitor for auto-wakeup of client machines
#
#    Copyright (C) 2011 Canonical Ltd.
#
#    Authors: Andres Rodriguez <andreserl@canonical.com>
#             Jim Heck <pinball.rules@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, threading
from logging import error, debug, info, warn
from scapy.all import *
#from scapy.all import sniff, ARP, Ether, IP, UDP, Raw, sendp

# Converts the MAC to some weird format
def mac_to_string(mac):
    return str(Ether(dst=mac))[:6]

# Create a WoL magic packet
def make_magic(sleeper_mac_str):
    return Ether(dst='ff:ff:ff:ff:ff:ff')/IP(dst='255.255.255.255')/UDP(dport=7)/Raw(load='\xff\xff\xff\xff\xff\xff' + sleeper_mac_str * 16)

class ARPMonitor(threading.Thread):

    # Initialise
    def __init__(self, config):
        threading.Thread.__init__(self)
        self._type = config['monitor']
        self._name = "ARP Monitor"
        self._arp_cache = config['cache']
        self._absent_seconds = 0
        self._running = False

    # Check for PIDs
    def active(self):
	return False 

    # Start thread
    def start(self):
        self._running = True
        threading.Thread.start(self)

    # Stop thread
    def stop(self):
        self._running = False

    def run(self):
        while self._running:
            sniff(prn=self.arp_wake_sleeper_callback, filter="arp", store=0)

    def arp_wake_sleeper_callback(self, pkt):
        # evaluates if received ARP packet with dest ip (pkt[ARP].pdst) is in cache
        if ARP in pkt and pkt[ARP].op == 1 and pkt[ARP].pdst in self._arp_cache:
            # If found in arp_cache, then try to wake up by sending a WoL.
            magic_pkt = make_magic(mac_to_string(self._arp_cache[pkt[ARP].pdst]))
            sendp(magic_pkt)
