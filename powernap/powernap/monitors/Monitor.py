#    powernapd plugin - Abastract monitor class
#
#    Copyright (C) 2009 Canonical Ltd.
#
#    Authors: Dustin Kirkland <kirkland@canonical.com>
#             Adam Sutton <dev@adamsutton.me.uk>
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

from logging import error, debug, info, warn
import time

# Abstract monitor
#   Note: it is not required that you subclass this, merely that you
#         provide a matching API (all functions are optional) 
class Monitor ( object ):

    # Initialise the object
    def __init__ ( self, config ):
        self._name     = self.__repr__()
        self._activity = 0
        self._grace    = 0
        self._period   = 60.0
        if ( 'name' in config   ): self._name   = config['name']
        if ( 'grace' in config  ): self._grace  = config['grace']
        if ( 'absent' in config ): self._period = config['absent']
        self.reset()

    # String representation for debug
    def __str__  ( self ): return self._name

    # Reset monitor (usually after resume)
    def reset  ( self ): self._activity = time.time()

    # Check if monitored resource is active
    def active ( self):
        ret      = False
        inactive = time.time() - self._activity
        if ( inactive < self._period ):
            debug('%s - inactive for %0.2f secs' % (str(self), inactive))
            ret = True
        return ret

    # Get preferred grace period
    def grace  ( self ): return self._grace

    # Start the monitor
    def start  ( self ): pass

    # Stop the monitor
    def stop   ( self ): pass

# ###########################################################################
# Editor directives
# ###########################################################################

# vim:sts=4:ts=4:sw=4:et
