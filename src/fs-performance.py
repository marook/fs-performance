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

import os
import optparse
import time

class StopWatch(object):

    def __init__(self):
        self.startTime = None
        self.stopTime = None

    def start(self):
        self.startTime = time.time()

    def stop(self):
        self.stopTime = time.time()

    @property
    def duration(self):
        if((self.startTime == None) or (self.stopTime == None)):
            return None

        return self.stopTime - self.startTime

    def __str__(self):
        return '%ss ' % self.duration

class Sensor(object):
    
    def __init__(self):
        self.measurements = []

    def startMeasurement(self):
        m = StopWatch()

        self.measurements.append(m)

        m.start()

        return m

    @property
    def min(self):
        v = None
        
        for m in self.measurements:
            d = m.duration

            if(d == None):
                continue

            if((v == None) or (d < v)):
                v = d

        return v

    @property
    def max(self):
        v = None
        
        for m in self.measurements:
            d = m.duration

            if(d == None):
                continue

            if((v == None) or (d > v)):
                v = d

        return v

    @property
    def average(self):
        measLen = len(self.measurements)

        if(measLen == 0):
            return None

        os = self.overallSum
        if(os == None):
            return None

        # TODO divide through the number of not None durations
        return os / measLen

    @property
    def median(self):
        ms = [m.duration for m in self.measurements if m.duration != None]

        ms.sort()

        msl = len(ms)
        if(msl == 0):
            return None

        if(msl % 2 == 0):
            return (ms[msl / 2] + ms[msl / 2 + 1]) / 2.0
        else:
            return ms[msl / 2]

    @property
    def overallSum(self):
        sum = 0.0

        for m in self.measurements:
            d = m.duration
            if(d == None):
                continue

            sum += d

        return sum

    def __str__(self):
        # TODO add median
        return '[measurements: %s, sum: %s, min: %ss, max: %ss, average: %ss, median: %ss]' % (len(self.measurements), self.overallSum, self.min, self.max, self.average, self.median)

class Profiling(object):

    def __init__(self):
        self.lsSensor = Sensor()

        self.overallStopWatch = StopWatch()
        self.overallStopWatch.start()

    def stop(self):
        self.overallStopWatch.stop()

    def __str__(self):
        return 'lsSensor: %s\nOverall time: %s\n' % (self.lsSensor, self.overallStopWatch)

def profileLs(profiling, path):
    w = profiling.lsSensor.startMeasurement()

    os.listdir(path)

    w.stop()

def profilePath(profiling, path):
    if(os.path.isdir(path)):
        profileLs(profiling, path)

    # TODO add further profilings

def main():
    usage = 'usage: %prog [options] target [commands]'
    parser = optparse.OptionParser()
    
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()

        return 1

    testRootPath = args[0]

    profiling = Profiling()

    retCode = 0
    try:
        def visit(arg, dirname, names):
            profilePath(profiling, dirname)

            for n in names:
                p = os.path.join(dirname, n)

                profilePath(profiling, p)

            # TODO profile names

        os.path.walk(testRootPath, visit, None)
    except KeyboardInterrupt:
        print 'User interrupted test'

        retCode = 1

    profiling.stop()

    print profiling

    return retCode

if __name__ == '__main__':
    import sys

    sys.exit(main())
