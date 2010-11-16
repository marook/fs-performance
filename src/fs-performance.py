#
# Copyright 2010 Markus Pielmeier
#
# This file is part of fs performance.
#
# fs performance is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fs performance is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fs performance.  If not, see <http://www.gnu.org/licenses/>.
#

import optparse
import time

class StopWatch(object):

    def __init__(self):
        self.start = time.time()

    def stop(self):
        self.stop = time.time()

def profilePath(path):
    pass

def main():
    usage = 'usage: %prog [options] target [commands]'
    parser = optparse.OptionParser()
    
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()

        return 1

    testRootPath = args[0]

    overallStopWatch = StopWatch()
    profilePath(testRootPath)
    overallStopWatch.stop()

    print "Overall time: %s" % overallStopWatch

if __name__ == '__main__':
    import sys

    sys.exit(main())
