#    powernapd plugin - Monitors process table for process with IO activity
#
#    Copyright (C) 2010, 2011 Canonical Ltd.
#
#    Authors: Dustin Kirkland <kirkland@canonical.com>
#             Adam Sutton <dev@adamsutton.me.uk>
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
import re
from logging import error, debug, info, warn, os
#from Monitor import Monitor

# Monitor plugin
#   looks for processes that have IO activity. Useful for some server
#   processes that are always present in the process list even when idle

# Looks for the process regex in /proc/<PID>/cmdline to obtain its PID(s).
# Optimal for processes that have a command line.
def find_pids_cmdline(regex):
    ret = []
    for d in os.listdir('/proc'):
        try:
            path = '/proc/%s/cmdline' % d
            if os.path.isfile(path):
                fp      = open(path)
                cmdline = fp.read()
                fp.close()
                if regex.search(cmdline):
                    ret.append(int(d))
        except:
            pass
    return ret

# Looks for the process regex in the "Name:" filed of /proc/<PID>/status
# to obtain its PID(s). Optimal for processes that do NOT have a command
# line. (i.e. NFS daemon processes.)
def find_pids_status(regex):
    ret = []
    for d in os.listdir('/proc'):
        try:
            path = '/proc/%s/status' % d
            if os.path.isfile(path):
                fp = open(path)
                status = fp.readline()
                fp.close()
                if regex.search(status.split()[1]):
                    ret.append(int(d))
        except:
            pass
    return ret

class IOMonitor ():

    # Initialise
    def __init__ ( self, config ):
        self._iocounts = {}
        self._type = config['monitor']
        self._name = config["name"]
        self._regex = re.compile(config['regex'])
        self._absent_seconds = 0

    def start(self):
        pass

    def active(self):
        if self.get_io_count():
            return True
        return False

    # Check for activity
    def get_io_count ( self ):

        # Get new PID list from processes with command line.
        pids = find_pids_cmdline(self._regex)
        # Processes with no command line result on an empty PID list.
        # if so, use alternate search method.
        if not pids:
            pids = find_pids_status(self._regex)

        # Get IO counts for all PIDs
        io_counts = {}
        for pid in pids:
            io_counts[pid] = {}
            try:
                fp = open('/proc/%d/io' % pid)
                for l in fp.readlines():
                    pts = l.split(':')
                    io_counts[pid][pts[0].strip()] = int(pts[1].strip())
                fp.close()
            except: pass # its possible the proc will die in here!

        ioactivity = False
        for pid in pids:
            # New process (assume activity)
            if pid not in self._iocounts:
                debug('    %s - adding new PID %d to list' % (self, pid))
            # Existing: check for change
            else:
                if (self._iocounts[pid]["write_bytes"] != io_counts[pid]["write_bytes"]) or \
                   (self._iocounts[pid]["read_bytes"] != io_counts[pid]["read_bytes"]):
                    ioactivity = True
                    self._iocounts[pid] = io_counts[pid]
                    break
            # Update count
            self._iocounts[pid] = io_counts[pid]

        if ioactivity:
            return True

        return False

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
