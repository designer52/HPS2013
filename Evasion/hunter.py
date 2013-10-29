import math

def playHunter(walls, movesToNextWallBuild, hunterDirection, hunterLocation, preyLocation, remainingTime):
  direction = hunterDirection
  relativeLocationOfPrey = getRelativeLocation(hunterLocation, preyLocation)

  wallToCreate = []
  wallToDestroy = []
  if getXDistance(hunterLocation, preyLocation) == 2:
    if hunterDirection == 'SE' and relativeLocationOfPrey == 'NE':
      wallToCreate = createVerticalWall(hunterLocation, walls)
    elif hunterDirection == 'SE' and relativeLocationOfPrey == 'SW':
      wallToCreate = createHorizontalWall(hunterLocation, walls)
    elif hunterDirection == 'SW' and relativeLocationOfPrey == 'NW':
      wallToCreate = createVerticalWall(hunterLocation, walls)
    elif hunterDirection == 'SW' and relativeLocationOfPrey == 'SE':
      wallToCreate = createHorizontalWall(hunterLocation, walls)

  if getYDistance(hunterLocation, preyLocation) == 2:
    if hunterDirection == 'NE' and relativeLocationOfPrey == 'NW':
      wallToCreate = createHorizontalWall(hunterLocation, walls)
    elif hunterDirection == 'NE' and relativeLocationOfPrey == 'SW':
      wallToCreate = createVerticalWall(hunterLocation, walls)
    elif hunterDirection == 'NW' and relativeLocationOfPrey == 'NE':
      wallToCreate = createHorizontalWall(hunterLocation, walls)
    elif hunterDirection == 'NW' and relativeLocationOfPrey == 'SW':
      wallToCreate = createVerticalWall(hunterLocation, walls)
  return (direction, wallToCreate, wallToDestroy)

def getDistance(first, second):
  return math.sqrt((first[0]-second[0])**2 + (first[1]-second[1])**2)

def getXDistance(first, second):
  return abs(first[0]-second[0])

def getYDistance(first, second):
  return abs(first[1]-second[1])

def getRelativeLocation(center, reference):
  # Quadrents are defined as follows:
  # 2 | 1
  # 3 | 4
  (xCenter, yCenter) = center
  (xReference, yReference) = reference

  if xCenter < xReference and yCenter > yReference:
    return 'NE'
  elif xCenter > xReference and yCenter > yReference:
    return 'NW'
  elif xCenter > xReference and yCenter < yReference:
    return 'SE'
  elif xCenter < xReference and yCenter < yReference:
    return 'SE'
  else:
    return 'Else'

def createVerticalWall(hunterLocation, walls):
  x = hunterLocation[0]
  minY = getWallCoordinate(hunterLocation, walls, 'min', 'y')
  maxY = getWallCoordinate(hunterLocation, walls, 'max', 'y')
  return [(x, minY), (x, maxY)]

def createHorizontalWall(hunterLocation, walls):
  y = hunterLocation[1]
  minX = getWallCoordinate(hunterLocation, walls, 'min', 'x')
  maxX = getWallCoordinate(hunterLocation, walls, 'max', 'x')
  return [(minX, y), (maxX, y)]

def getWallCoordinate(hunterLocation, walls, minMax, xY):
  (xHunter, yHunter) = hunterLocation
  if minMax == 'min':
    if xY == 'x':
      possibleX = [x1+1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if yHunter in range(y1, y2+1)
                   if xHunter > x1]
      return max(possibleX+[0])
    elif xY == 'y':
      possibleY = [y1+1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if xHunter in range(x1, x2+1)
                   if yHunter > y1]
      return max(possibleY+[0])
  elif minMax == 'max':
    if xY == 'x':
      possibleX = [x1-1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if yHunter in range(y1, y2+1)
                   if xHunter < x1]
      return min(possibleX+[499])
    elif xY == 'y':
      possibleY = [y1-1
                   for (_, (x1, y1), (x2, y2)) in walls
                   if xHunter in range(x1, x2+1)
                   if yHunter < y1]
      return min(possibleY+[499])
