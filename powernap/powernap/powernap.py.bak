#!/usr/bin/python
#
#    powernap.py - handles powernap's config and initializes Monitors.
#
#    Copyright (C) 2010 Canonical Ltd.
#
#    Authors: Andres Rodriguez <andreserl@ubuntu.com>
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
from monitors import ProcessMonitor, LoadMonitor, InputMonitor, TCPMonitor, UDPMonitor, IOMonitor, WoLMonitor, ConsoleMonitor, DiskMonitor


class PowerNap:

    def __init__(self):
        self.PKG = "powernap"
        self.CONFIG = "/etc/powernap/config"
        self.ACTION = "/usr/sbin/powernap"
        self.RECOVER_ACTION = "/usr/sbin/pm-powersave false"
        self.ABSENT_SECONDS = sys.maxint
        self.STAGE2_ABSENT_SECONDS = sys.maxint
        self.INTERVAL_SECONDS = int(1)
        self.GRACE_SECONDS = int(60)
        self.DEBUG = int(0)
        self.ACTION_METHOD = 0
        self.STAGE2_ACTION_METHOD = 4
        self.MONITORS = []
        self.WARN = False
        self.WATCH_CONFIG = False
        self.KERN_MODULES = {}
        self.SERVICES = {}
        self.stage2_action_enabled = False
        # Load default config file (/etc/powernap/config)
        self.load_config_file()

    def load_config_file(self):
        stage2_section = "%s-stage2" % self.PKG
        cfg = ConfigParser.ConfigParser()
        cfg.read(self.CONFIG)

        try:
            # Load items in DEFAULT section
            defaults = cfg.items(self.PKG)
            for items in defaults:
                self.set_default_values(items[0], items[1])

            stage2 = cfg.items(stage2_section)
            for items in stage2:
                self.set_stage2_values(items[0], items[1])

            # Load items on each monitor
            monitors_config = cfg.sections()
            for monitor in monitors_config:
                if monitor not in [self.PKG, stage2_section]:
                    for items in cfg.items(monitor):
                        self.load_monitors_config(monitor, items)
        except:
            pass

        # Load extra config files (/etc/powernap/config.d/*)
        configd = "/etc/%s/config.d" % self.PKG
        if os.path.exists(configd):
            for config in os.listdir(configd):
                self.load_configd_files("%s/%s" % (configd, config))

    def load_configd_files(self, config_file):
        cfg = ConfigParser.ConfigParser()
        cfg.read(config_file)

        try:
            monitors_config = cfg.sections()
            for monitor in monitors_config:
                for items in cfg.items(monitor):
                    for i in range(len(self.MONITORS)):
                        if self.MONITORS[i]['monitor'] == monitor and self.MONITORS[i]['name'] == items[0]:
                            self.MONITORS.pop(i)
                            break
                    self.load_monitors_config(monitor, items)
        except:
            pass

    def set_default_values(self, var, value):
        if var == "absent_seconds":
            self.ABSENT_SECONDS = eval(value)
        if var == "interval_seconds":
            self.INTERVAL_SECONDS = eval(value)
        if var == "grace_seconds":
            self.GRACE_SECONDS = eval(value)
        if var == "debug":
            self.DEBUG = eval(value)
        if var == "action":
            self.ACTION = eval(value)
        if var == "action_method":
            self.ACTION_METHOD = eval(value)
        if var == "warn":
            if value == "y" or value == "yes":
                self.WARN = True
            else:
                self.WARN = False
        if var == "watch_config":
            if value == "y" or value == "yes":
                self.WATCH_CONFIG = True
            else:
                self.WATCH_CONFIG = False
        if var == "kern_modules":
            self.KERN_MODULES = value.split()
        if var == "services":
            self.SERVICES = value.split()

    def set_stage2_values(self, var, value):
        if var == "stage2_action_method":
            self.STAGE2_ACTION_METHOD = eval(value)
        if var == "stage2_absent_seconds":
            self.STAGE2_ABSENT_SECONDS = eval(value)
            if self.STAGE2_ABSENT_SECONDS > 0:
                self.stage2_action_enabled = True

    def usb_input_available(self, event):
        regex = re.compile(event)
        path = "/dev/input/by-id"
        exists = False

        for str in os.listdir(path):
            match = regex.search(str)
            if match:
                exists = True
                break
        return exists

    def load_monitors_config(self, monitor, items):
        if monitor == "ProcessMonitor" or monitor == "IOMonitor":
            self.MONITORS.append({"monitor":monitor, "name":items[0], "regex":eval(items[1]), "absent":self.ABSENT_SECONDS})
        if monitor == "InputMonitor" and (items[1] == "y" or items[1] == "yes"):
            if items[0] == "mouse" and self.usb_input_available("mouse"):
                self.MONITORS.append({"monitor":monitor, "name":items[0], "regex":"mice"})
            elif items[0] == "keyboard" and self.usb_input_available("kbd"):
                self.MONITORS.append({"monitor":monitor, "name":items[0], "regex":"kbd"})
            #else:
            #    self.MONITORS.append({"monitor":monitor, "name":items[0], "regex":items[1]})
        if monitor == "ConsoleMonitor" and (items[1] == "y" or items[1] == "yes"):
            self.MONITORS.append({"monitor":monitor, "name":items[0]})
        if monitor == "LoadMonitor":
            self.MONITORS.append({"monitor":monitor, "name":items[0], "threshold":items[1]})
        if monitor == "TCPMonitor":
            self.MONITORS.append({"monitor":monitor, "name":items[0], "port":items[1], "absent":self.ABSENT_SECONDS})
        if monitor == "UDPMonitor":
            # If ACTION_METHOD is 0 (PowerSave) and port is 7 or 9, do *NOT* create a monitor
            # This will cause that the WoL monitor to not be able to bind the port or viceversa.
            # TODO: Display a message that port is not being binded!!
            if self.ACTION_METHOD == 0 and (items[1] != 7 or items[1] != 9):
                self.MONITORS.append({"monitor":monitor, "name":items[0], "port":eval(items[1]), "absent":self.ABSENT_SECONDS})
        if monitor == "WoLMonitor":
            self.MONITORS.append({"monitor":monitor, "name":items[0], "port":eval(items[1]), "absent":self.ABSENT_SECONDS})
        if monitor == "DiskMonitor" and (items[1] == "y" or items[1] == "yes"):
            self.MONITORS.append({"monitor":monitor, "name":items[0], "absent":self.ABSENT_SECONDS})

    def get_monitors(self):
        monitor = []
        for config in self.MONITORS:
            if config["monitor"] == "ProcessMonitor":
                p = ProcessMonitor.ProcessMonitor(config)
            if config["monitor"] == "LoadMonitor":
                p = LoadMonitor.LoadMonitor(config)
            if config["monitor"] == "UDPMonitor":
                p = UDPMonitor.UDPMonitor(config)
            if config["monitor"] == "WoLMonitor":
                p = WoLMonitor.WoLMonitor(config)
            if config["monitor"] == "InputMonitor":
                p = InputMonitor.InputMonitor(config)
            if config["monitor"] == "ConsoleMonitor":
                p = ConsoleMonitor.ConsoleMonitor(config)
            if config["monitor"] == "IOMonitor":
                p = IOMonitor.IOMonitor(config)
            if config["monitor"] == "TCPMonitor":
                p = TCPMonitor.TCPMonitor(config)
            if config["monitor"] == "DiskMonitor":
                p = DiskMonitor.DiskMonitor(config)
            monitor.append(p)

        return monitor
