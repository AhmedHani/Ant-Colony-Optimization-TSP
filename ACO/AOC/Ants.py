class Ants(object):
    """Ants data structure"""
    tourLength = float;
    path = [];
    visited = [];
    currentCity = int;
    nextCity = int;
    pathIndex = int;

    def __init__(self, tourLength, path, pathIndex, currentCity, nextCity, visited):
        self.path = path;
        self.pathIndex = pathIndex;
        self.visited = visited;
        self.tourLength = tourLength;
        self.currentCity = currentCity;
        self.nextCity = nextCity;

    def __repr__(self):
        return repr((self.tourLength, self.path, self.visited, self.currentCity, self.nextCity, self.pathIndex))


        


