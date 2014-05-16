import matplotlib.pyplot as plt
from numpy import *
from City import *
from Ants import *
import math
from random import randint
import Globals
import copy as cp
from operator import itemgetter, attrgetter

allCities = [City(0, 0) for i in range(Globals.MAX_CITIES)]

allAnts = [Ants(0, 0, 0, 0, 0, 0) for i in range(Globals.MAX_ANTS)]
rankedAnts = [Ants(0, 0, 0, 0, 0, 0) for i in range(Globals.MAX_ANTS)]

distance = [[0.0 for i in range(Globals.MAX_CITIES)] for j in range(Globals.MAX_CITIES)]
phermones = [[0.0 for i in range(Globals.MAX_CITIES)] for j in range(Globals.MAX_CITIES)]

bestAnt = 0
global bestTour 
bestTour = Globals.MAX_TOUR

def calculateDistance(x2, x1, y2, y1):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));

def getDistance():
    for i in range(Globals.MAX_CITIES):
        for j in range(Globals.MAX_CITIES):
            if i != j and distance[i][j] == 0.0:
                distance[i][j] = distance[j][i] = calculateDistance(int(allCities[j].xCoordinate), int(allCities[i].xCoordinate),
                                                   int(allCities[j].yCoordinate), int(allCities[i].yCoordinate));
   
def InitializeGraph():
    file = open('Graph.txt', 'r');

    for i in range(Globals.MAX_CITIES):
        allCities[i].xCoordinate = int(file.readline());
        allCities[i].yCoordinate = int(file.readline());

    for i in range(Globals.MAX_CITIES):
        for j in range(Globals.MAX_CITIES):
            distance[i][j] = 0.0;
            phermones[i][j] = Globals.INITIAL_PHERMONES;
    
    getDistance();
    
def InitializeAnts():
    second = 0;

    for ant in range(Globals.MAX_ANTS):
        allAnts[ant].visited = [False for i in range(Globals.MAX_CITIES)];
        allAnts[ant].path = [-1 for i in range(Globals.MAX_CITIES)];

    for ant in range(Globals.MAX_ANTS):
        if second == Globals.MAX_CITIES:
            second = 0;

        allAnts[ant].currentCity = second;
        second += 1;
        
        for i in range(Globals.MAX_CITIES):
            allAnts[ant].path[i] = -1;
            allAnts[ant].visited[i] = False;
        
        allAnts[ant].pathIndex = 1;
        allAnts[ant].path[0] = allAnts[ant].currentCity;
        allAnts[ant].nextCity = -1;
        allAnts[ant].tourLength = 0.0;
        allAnts[ant].visited[allAnts[ant].currentCity] = True;    

    for ant in range(Globals.MAX_ANTS):
        rankedAnts[ant].visited = [False for i in range(Globals.MAX_ANTS)];
        rankedAnts[ant].path = [-1 for i in range(Globals.MAX_ANTS)];


def reInitializeAnts():
    second = 0;
    global bestTour
    for ant in range(Globals.MAX_ANTS):
        if allAnts[ant].tourLength < bestTour:
            bestTour = allAnts[ant].tourLength;
            bestAnt = ant;

        allAnts[ant].nextCity = -1;
        allAnts[ant].tourLength = 0.0;

        allAnts[ant].visited = [False for i in range(Globals.MAX_CITIES)];
        allAnts[ant].path = [-1 for i in range(Globals.MAX_CITIES)];
        
        if second == Globals.MAX_CITIES:
            second = 0;
        
        allAnts[ant].currentCity = second;
        second += 1;
        allAnts[ant].pathIndex = 1;
        allAnts[ant].path[0] = allAnts[ant].currentCity;
        allAnts[ant].visited[allAnts[ant].currentCity] = True;     

def bestWayFormula(first, second):
    if (math.fabs(distance[first][second]) > 0): 
        return (((math.pow(phermones[first][second], Globals.ALPHA) * math.pow((1.0 / distance[first][second]), Globals.BETA))));
    else:
        return 0;

def nextTrip(ant):
    drones = 0.0;
    second = 0;
    probability = 0.0;
    first = allAnts[ant].currentCity;

    for second in range(Globals.MAX_CITIES):
        if not allAnts[ant].visited[second]:
            drones += bestWayFormula(first, second);
    second = 0;

    while True:
        second += 1;
        if second >= Globals.MAX_CITIES:
            second = 0;
        if not allAnts[ant].visited[second]:
            probability = bestWayFormula(first, second) / drones;
            flag = float(randint(0, 32767)) / 32767;
            if flag < probability:
                break;

    return second;

def antsMovements():
    moves = 0;

    for ant in range(Globals.MAX_ANTS):
        if allAnts[ant].pathIndex < Globals.MAX_CITIES:
            moves += 1;
            allAnts[ant].nextCity = nextTrip(ant);
            allAnts[ant].visited[allAnts[ant].nextCity] = True;
            allAnts[ant].path[allAnts[ant].pathIndex] = allAnts[ant].nextCity;
            allAnts[ant].pathIndex += 1;
            allAnts[ant].tourLength += distance[allAnts[ant].currentCity][allAnts[ant].nextCity];

            #handles the path between the end and start node
            if allAnts[ant].pathIndex == Globals.MAX_CITIES:
                allAnts[ant].tourLength += distance[allAnts[ant].path[Globals.MAX_CITIES - 1]][allAnts[ant].path[0]];

            allAnts[ant].currentCity = allAnts[ant].nextCity;

    return moves;



def antRanking():
    #rankedAnts = cp.copy(allAnts);
    for i in range(Globals.MAX_CITIES):
       rankedAnts[i] = allAnts[i];
    
    temp = Ants;
    for i in range(Globals.MAX_CITIES):
        for j in range(i + 1, Globals.MAX_CITIES):
             if rankedAnts[i].tourLength > rankedAnts[j].tourLength:
                 temp = rankedAnts[i];
                 rankedAnts[i] = rankedAnts[j];
                 rankedAnts[j] = temp;

     # sorted(rankedAnts, key=lambda Ants: Ants.tourLength);


def trailsUpdate():
    for first in range(Globals.MAX_CITIES):
        for second in range(Globals.MAX_CITIES):
            if first != second:
                phermones[first][second] *= (1.0 - Globals.EVAPOURATION_RATE);
                if phermones[first][second] < 0.0:
                    phermones[first][second] = Globals.INIT_PHER;

    first = 0;
    second = 0;
    for ant in range(int(Globals.RANK_WEIGHT - 1)):
        for idx in range(Globals.MAX_CITIES):
            if idx < Globals.MAX_CITIES - 1:
                first = rankedAnts[ant].path[idx];
                second = rankedAnts[ant].path[idx + 1];
            else:
                first = rankedAnts[ant].path[idx];
                second = rankedAnts[ant].path[0];
           
            phermones[first][second] += (Globals.RANK_WEIGHT - ant) * (Globals.Q /  rankedAnts[ant].tourLength);
            phermones[second][first] = phermones[first][second];

    first = 0;
    second = 0;
    for idx in range(Globals.MAX_CITIES):
        if idx < Globals.MAX_CITIES - 1:
            first = rankedAnts[bestAnt].path[idx];
            second = rankedAnts[bestAnt].path[idx + 1];
        else:
            first = rankedAnts[bestAnt].path[idx];
            second = rankedAnts[bestAnt].path[0];

        phermones[first][second] += (Globals.Q / bestTour);
        phermones[second][first] =  phermones[first][second];

    for first in range(Globals.MAX_CITIES):
        for second in range(Globals.MAX_CITIES):
            phermones[first][second] *= Globals.EVAPOURATION_RATE;

def showData():
    theBestAnt = allAnts[bestAnt];
    x0, y0, x1, y1 = [], [], [], []
   
    ln = 0;
    for i in range(Globals.MAX_CITIES):
        tmp = int(theBestAnt.path[i])
        if tmp != -1:
            ln += 1; 

    for i in range(Globals.MAX_CITIES):
        x0.append(allCities[i].xCoordinate)
        y0.append(allCities[i].yCoordinate)

    plt.plot(x0, y0, marker='*', linestyle='-', color='aqua')

    for i in range(ln):
        x1.append(allCities[theBestAnt.path[i]].xCoordinate)
        y1.append(allCities[theBestAnt.path[i]].yCoordinate)

    x1.append(allCities[theBestAnt.path[0]].xCoordinate)
    y1.append(allCities[theBestAnt.path[0]].yCoordinate)

    plt.plot(x1,y1, marker='*', linestyle='--', color='r')
    
    for i in range(ln):
        plt.text(x1[i], y1[i], theBestAnt.path[i])
        print theBestAnt.path[i], " " 
        
    plt.show()
    

def main():
    InitializeGraph();
    InitializeAnts()
    
    for currentTime in range(1, Globals.MAX_TIME):
        if not antsMovements():
            antRanking()
            trailsUpdate();
            if currentTime != Globals.MAX_TIME:
                reInitializeAnts();

            print currentTime, bestTour
    
    print "\n", bestTour

    showData()

main()



     