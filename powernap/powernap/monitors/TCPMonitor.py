#    powernapd plugin - Monitors network for open tcp connections
#
#    Copyright (C) 2011 Canonical Ltd.
#
#    Authors: Dustin Kirkland <kirkland@canonical.com>
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

import os, re, subprocess
from logging import error, debug, info, warn

# True if an network connection matches 
def find_connection(netstat, regexes):
    for regex in regexes:
        for str in netstat:
            if regex.search(str):
                return True
    return False

class TCPMonitor():

    # Initialise
    def __init__(self, config):
        self._type = config['monitor']
        self._name = config['name']
        self._absent_seconds = 0
        self._regexes = []
        port_start = int(config['port'].split("-")[0].strip())
        port_end = int(config['port'].split("-")[-1].strip()) + 1 # Add one to use correctly in range
        for port in range(port_start, port_end):
            self._regexes.append(re.compile("^tcp.*\W.*:%s\W.*ESTABLISHED$" % port))

    # Check for connections
    def active(self):
        ps = subprocess.getoutput("netstat -Wnt").splitlines()
        if find_connection(ps, self._regexes):
           return True
        return False

    def start(self):
        pass

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
