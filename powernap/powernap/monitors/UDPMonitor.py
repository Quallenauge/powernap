#    powernapd plugin - Monitors a UDP socket for data
#
#    Copyright (C) 2011 Canonical Ltd.
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

import threading, time
from logging import error, debug, info, warn

# Monitor plugin
#   listen for data on a UDP socket (typically WOL packets)
class UDPMonitor (threading.Thread):

    # Initialise
    def __init__ ( self, config ):
        threading.Thread.__init__(self)
        self._type = config['monitor']
        self._name = config['name']
        self._port = config['port']
        self._running = False
        self._data_received = False
        self._absent_seconds = 0

    # Start thread
    def start ( self ):
      self._running = True
      threading.Thread.start(self)

    # Stop thread
    def stop ( self ): self._running = False

    # Open port and wait for data (any data will trigger the monitor)
    def run ( self ):
        import socket

        # Create socket
        sock   = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listen = False

        while self._running:
            if not listen:
                try:
                    debug('%s - configure socket' % self)
                    sock.bind(('', self._port))
                    sock.settimeout(1.0)
                    listen = True
                except Exception as e:
                    error('%s - failed to config socket [e=%s]' % (self, str(e)))
                    time.sleep(1.0)
            else:
                try:
                    # Wait for data
                    sock.recvfrom(1024)
                    self._data_received = True
                    debug('%s - data packet received' % self)
                    self.reset()
                except: pass # timeout

    def active(self):
        if self._data_received:
            self._data_received = False
            return True
        return False

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
