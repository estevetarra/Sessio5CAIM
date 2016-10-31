#!/usr/bin/python

from collections import namedtuple
import operator
import time
import sys
import math

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = [] #vector of edges
        self.routeHash = dict()
        self.outweight =  0 

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

edgeHash = dict() # hash of edge to ease the match
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
    print "Reading Airport file from {0}".format(fd)
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5:
                raise Exception('not an IATA code')            
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            #print a
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
        except Exception as inst:
            print "Exception"
            pass
        else:
            if destin in airportHash and origin in airportHash:
                cont += 1
                if not destin in edgeHash:
                    edgeHash[destin] = {}
                    edgeHash[destin][origin] = 1
                elif not origin in edgeHash[destin]:
                    edgeHash[destin][origin] = 1
                else:
                    edgeHash[destin][origin] += 1
                airportHash[origin].outweight += 1
            else:
                # Origin or destination airport in the route was not in the airports file one. 
                # It is ok to get rid of this route.
                pass
    routesTxt.close()
    print "There were {0} valid edges ".format(cont)

def computePageRanks():
    n = len(airportHash)
    P = {airport_name: 1.0/n for airport_name in airportHash}
    L = 0.8
    i = 0
    # extra contribution to each position of P due to airports with outweight 0.
    num_airports_outweight_0 = 0
    for airport_name, airport in airportHash.iteritems():
        if airport.outweight == 0:
            num_airports_outweight_0 += 1
    difference = float('Inf')
    while difference > 1e-5:
        Q = {airport_name: 0.0 for airport_name in airportHash}
        extra = 0.0
        for destin in airportHash:
            if airportHash[destin].outweight == 0:
                extra += P[destin]*L*1.0/n
            if destin in edgeHash: 
                # current airport has incoming routes
                for origin, weight in edgeHash[destin].iteritems():
                    Q[destin] += L*P[origin]*weight/airportHash[origin].outweight
            
            Q[destin] += (1-L)/n
        Q = {destin: score + extra for destin, score in Q.iteritems()}
        difference = math.sqrt(sum([(Q[airport_name]-P[airport_name])**2 for airport_name in Q]))
        # suma = 0.0
        # for k,v in Q.iteritems():
        #     suma += v
        # print suma
        P = Q
        i += 1
    return (i, P)

def outputPageRanks(pageranks):
    sorted_pageranks = sorted(pageranks.items(), key=operator.itemgetter(1), reverse = True)
    print_list = [(pagerank, airportHash[code].name) for code, pagerank in sorted_pageranks]
    with open('pagerank_output.txt', 'w') as fp:
        fp.write('\n'.join('%s %s' % x for x in print_list)) 
    return print_list 


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations, pageranks = computePageRanks()
    time2 = time.time()
    print_list = outputPageRanks(pageranks)
    print "#Iterations:", iterations
    print "Time of computePageRanks():", time2-time1
    print "Final Pagerank: ", print_list[1:20]


if __name__ == "__main__":
    sys.exit(main())
