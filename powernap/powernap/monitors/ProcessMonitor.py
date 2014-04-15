#    powernapd plugin - Monitors process table for presence of process
#
#    Copyright (C) 2011 Canonical Ltd.
#
#    Authors: Dustin Kirkland <kirkland@canonical.com>
#             Andres Rodriguez <andreserl@canonical.com>
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

# Find list of PIDs that match a given regex (cmdline)
def find_process(ps, regex):
    for str in ps:
        if regex.search(str):
            return 1
    return 0

class ProcessMonitor():

    # Initialise
    def __init__(self, config):
        self._type = config['monitor']
        self._name = config['name']
        self._regex = re.compile(config['regex'])
        self._absent_seconds = 0

    # Check for PIDs
    def active(self):
        ps = subprocess.getoutput("ps -eo args").splitlines()
        if find_process(ps, self._regex):
               return True
        return False

    def start(self):
        pass

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
