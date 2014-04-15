#!/usr/bin/python
#
#    powerwake.py - handles powerwaked config and initializes Monitors.
#
#    Copyright (C) 2011 Canonical Ltd.
#
#    Authors: Andres Rodriguez <andreserl@canonical.com>
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

import ConfigParser, sys, re, os
#from monitors import ARPMonitor 

class PowerWake:

    def __init__(self):
        self.PKG = "powerwake"
        self.CONFIG = "/etc/powernap/powerwaked.conf"
        self.ACTION = "/usr/bin/powerwake"
        self.INTERVAL_SECONDS = int(1)
        self.DEBUG = int(0)
        self.MONITORS = []
        # Load default config file (/etc/powernap/config)
        self.load_config_file()

    def load_config_file(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read(self.CONFIG)

        try:
            # Load items in DEFAULT section
            defaults = cfg.items(self.PKG)
            for items in defaults:
                self.set_default_values(items[0], items[1])

            monitors_config = cfg.sections()
            for monitor in monitors_config:
                for items in cfg.items(monitor):
                    self.load_monitors_config(monitor, items)
        except:
            pass

    def set_default_values(self, var, value):
        if var == "interval_seconds":
            self.INTERVAL_SECONDS = eval(value)
        if var == "debug":
            self.DEBUG = eval(value)
        if var == "action":
            self.ACTION = eval(value)
        if var == "warn":
            if value == "y" or value == "yes":
                self.WARN = True

    def load_monitors_config(self, monitor, items):
        if monitor == "ARPMonitor" and (items[1] == "y" or items[1] == "yes"):
            self.MONITORS.append({"monitor":monitor, "cache":self.get_monitored_hosts(monitor.lower())})

    def get_monitors(self):
        from monitors import ARPMonitor 
        monitor = []
        for config in self.MONITORS:
            if config["monitor"] == "ARPMonitor":
                p = ARPMonitor.ARPMonitor(config)
            monitor.append(p)

        return monitor

    def get_monitored_hosts(self, monitor):
        host_to_mac = {}
        for file in ["/etc/powernap/powerwaked.%s.ethers" % monitor]:
            if os.path.exists(file):
                f = open(file, 'r')
                for i in f.readlines():
                    try:
                        (m, h) = i.split()
                        host_to_mac[h] = m
                    except:
                        pass
                f.close()
        return host_to_mac

    def set_monitored_hosts(self, host_to_mac, monitor):
        path = ["/etc/powernap/powerwaked.%s.ethers" % monitor]
        for file in path:
            if not os.path.exists(file):
                f = open(file, 'a')
                f.close()
        for file in ["/etc/powernap/powerwaked.%s.ethers" % monitor]:
            if os.access(file, os.W_OK):
                f = open(file, 'w')
                for h in host_to_mac:
                    if self.is_mac(host_to_mac[h]):
                        f.write("%s %s\n" % (host_to_mac[h], h))
                f.close()

    def get_mac_or_ip_from_arp(self, host):
        mac_or_ip = None
        for i in os.popen("/usr/sbin/arp -n"):
            m = i.split()[2]
            h = i.split()[0]
            if self.is_mac(host) and host == m and self.is_ip(h):
                mac_or_ip = h
                break
            if self.is_ip(host) and host == h and self.is_mac(m):
                mac_or_ip = m
                break
        #if not mac_or_ip:
        #    raise BaseException("Error")
        return mac_or_ip

    def is_ip(self, ip):
        r1 = re.compile('^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$')
        if r1.match(ip):
            return True
        else:
            return False

    def is_mac(self, mac):
        r1 = re.compile('^[0-9a-fA-F]{12}$')
        r2 = re.compile('^[0-9a-fA-F]{2}.[0-9a-fA-F]{2}.[0-9a-fA-F]{2}.[0-9a-fA-F]{2}.[0-9a-fA-F]{2}.[0-9a-fA-F]{2}$')
        if r1.match(mac) or r2.match(mac):
            return 1
        else:
            return 0

#### --------------------------------- from powerwake --------------------------------####

    # Source the cached, known arp entries
    def get_arp_cache(self):
        host_to_mac = {}
        #for file in ["/var/cache/%s/ethers" % self.PKG, "/etc/ethers", "%s/.cache/ethers" % HOME]:
        for file in ["/var/cache/%s/ethers" % self.PKG, "/etc/ethers"]:
            if os.path.exists(file):
                f = open(file, 'r')
                for i in f.readlines():
                    try:
                        (m, h) = i.split()
                        host_to_mac[h] = m
                    except:
                        pass
                f.close()
        return host_to_mac

    # Source the current, working arp table
    def get_arp_current(self, host_to_mac):
        # Load hostnames
        for i in os.popen("/usr/sbin/arp"):
            m = i.split()[2]
            h = i.split()[0]
            if is_mac(m):
                host_to_mac[h] = m
        # Load ip addresses
        for i in os.popen("/usr/sbin/arp -n"):
            m = i.split()[2]
            h = i.split()[0]
            if is_mac(m):
                host_to_mac[h] = m
        return host_to_mac

    def write_arp_cache(self, host_to_mac):
        if not os.access("%s/.cache/" % HOME, os.W_OK):
            return
        if not os.path.exists("%s/.cache/" % HOME):
            os.makedirs("%s/.cache/" % HOME)
        f = open("%s/.cache/ethers" % HOME, 'a')
        f.close()
        for file in ["/var/cache/%s/ethers" % PKG, "%s/.cache/ethers" % HOME]:
            if os.access(file, os.W_OK):
                f = open(file, 'w')
                for h in host_to_mac:
                    if self.is_mac(host_to_mac[h]):
                        f.write("%s %s\n" % (host_to_mac[h], h))
                f.close()
