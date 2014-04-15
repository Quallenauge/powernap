#    powernapd plugin - Monitors disk power state
#
#    Copyright (C) 2011 Jim Heck.
#
#    Authors: Jim Heck <pinball.rules@gmail.com>
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
import re, subprocess
from logging import error, debug, info, warn

# Monitor plugin
#   looks for disks that are active/idle.  Useful for sleeping only when
#   specified disks are in standby

class DiskMonitor ():

    # Initialise
    def __init__(self, config):
        self._type = config['monitor']
        self._name = config['name']
        self._regex_state = re.compile(r"^\s+drive\s+state\s+is:\s+(\S+)")
        self._regex_not_found = re.compile(r"^.*No\s+such\s+file")
        self._absent_seconds = 0

    def start(self):
        pass

    def active(self):
        if self.is_disk_active():
            return True
        return False

    # Check for inactive drive by looking explicitly for drive state of
    # 'standby' or 'sleeping'.  Assume 'active/idle', except in case
    # where fuction returns 'No such file' error (e.g. unknown drive)
    def is_disk_active(self):
        hdparm = subprocess.getoutput("hdparm -C /dev/%s" % self._name).splitlines()
        is_active = True
        for line in hdparm:
            if self._regex_not_found.match(line):
                #warn("    Disk monitor: disk %s not found, ignoring" % self._name)
                return False
            if self._regex_state.match(line):
                state = self._regex_state.search(line).group(1)
                #debug("    Disk monitor: disk %s in state %s" % (self._name, state))
                if state == 'standby' or state == 'sleeping':
                    is_active = False
        if is_active:
            return True
        return False


# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
