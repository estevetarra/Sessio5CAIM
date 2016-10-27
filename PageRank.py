#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin # write appropriate value
        self.weight = 1 # write appropriate value

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = [] #vector of edges
        self.routeHash = dict()
        self.outweight =  -1  # write appropriate value
	self.pageIndex = -1

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
	    temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')            
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            #print a
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print "There were {0} Airports with IATA code".format(cont)


def readRoutes(fd):
    print "Reading Routes file from {0}".format(fd)
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try:
	    temp = line.split(',')
	    if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')            
            origin = temp[2]
            destin = temp[4]
            e = Edge(origin)
            print airportHash[destin].routes
            
            #r.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            #r.code=temp[4][1:-1]
        except Exception as inst:
	    print "Exeption"
            pass
        else:
            cont += 1
            #edgeList.append(r)
            #airportHash[r.code] = r
    routesTxt.close()
    print "There were {0} valid edges ".format(cont)
    # write your code

def computePageRanks():
    return 0
    # write your code

def outputPageRanks():
    return 0
    # write your code

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    #outputPageRanks()
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1


if __name__ == "__main__":
    sys.exit(main())