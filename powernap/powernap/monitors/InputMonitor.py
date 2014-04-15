#    powernapd plugin - Monitors /dev/input for user activity
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

import os, re, threading
import select
from fcntl import fcntl, F_NOTIFY, DN_CREATE, DN_DELETE, DN_MULTISHOT
from logging import error, debug, info, warn

# Monitor plugin
#   Monitors devices in /dev/input for activity
class InputMonitor ( threading.Thread ):

    # Initialise
    def __init__ ( self, config ):
        threading.Thread.__init__(self)
        self._type = config['monitor']
        self._name = config['name']
        self._absent_seconds = 0
        self._input_received = False

        # If regex is in the way of by-id/regex, then path is changed to /dev/input/by-id
        if os.path.split(config['regex'])[0]:
            self._path = os.path.join("/dev/input", os.path.dirname(config['regex']))
            self._regex = re.compile(os.path.basename(config['regex']))
        elif config["regex"] == "kbd":
            self._path = "/dev/input/by-id"
            self._regex = re.compile(config['regex'])
        else:
            self._path = "/dev/input"
            self._regex = re.compile(config['regex'])

        # Register for directory events / setup input watches
        self._inputs = {}
        self._poll   = select.poll()
        self._update_inputs()
        self._dd     = os.open(self._path, 0)
        fcntl(self._dd, F_NOTIFY, DN_DELETE | DN_CREATE | DN_MULTISHOT)

    # Update the input events list
    def _update_inputs ( self ):
        events = {}
        event = None # Name of the event to poll, after finding it
        evpath = None # Absolute path of the event to poll

        # Search for the event in path:
        for str in os.listdir(self._path):
            match = self._regex.search(str)
            if match:
                event = str
                evpath = os.path.abspath(os.path.join(self._path, event))
                break

        # If event is different from None, then update!
        if event:
           if os.path.exists(evpath):
              fp = open(evpath)
              events[evpath] = fp
              # Register the event to poll
              self._poll.register(fp.fileno(), select.POLLIN|select.POLLPRI)
              self._inputs = events

    # Start the thread
    def start ( self ):
        self._running = True
        threading.Thread.start(self)

    # Stop thread
    def stop ( self ): self._running = False

    # Monitor /dev/input
    def run ( self ):

        # Poll for events
        while self._running:
            res = self._poll.poll(1000)
            if ( res ):
                for fd, e in res:
                    if e & (select.POLLIN|select.POLLPRI):
                        os.read(fd, 32768) # Read what is there!
                        self._input_received = True

    def active(self):
        if self._input_received:
            self._input_received = False
            return True
        return False

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
