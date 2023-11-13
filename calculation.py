import math
import numpy as np


def coordinatesAfterTurn(coordinates, corner):
    #truncate matrix
    a = math.radians(corner[0])
    b = math.radians(corner[1])
    c = math.radians(corner[2])
    coordinates = np.trunc(np.array(coordinates))
    turn_matrix = np.array([
    [math.cos(b)*math.cos(c), -math.sin(c)*math.cos(b), math.sin(b)],
    [math.sin(a)*math.sin(b)*math.cos(c) + math.sin(c)*math.cos(a),
    -math.sin(a) * math.sin(b)*math.sin(c) + math.cos(a)*math.cos(c),
    -math.sin(a) * math.cos(b)],
    [math.sin(a)*math.sin(c) - math.sin(b) * math.cos(a) * math.cos(c),
    math.sin(a)*math.cos(c) + math.sin(b) * math.sin(c) * math.cos(a),
    math.cos(a)*math.cos(b)]
    ])
    coordinates = np.dot(coordinates, turn_matrix)
    newX, newY, newZ = coordinates[0], coordinates[1], coordinates[2]
    newCoordinates = [newX, newY, newZ]
    return newCoordinates


def turnFigures(polygons, corner, X, Y,):
    # figureNormal = changeFigureSystemCoordinate(figure, X, Y, 'toNormal')
    # pointNormal = changePointSystemCoordinates(point, X, Y, 'toNormal')
    newFigures = []
    for p in polygons:
        new_poly = []
        for dots in p:
            newPoint = coordinatesAfterTurn(dots, corner)
            new_poly.append(list(newPoint))
        newFigures.append(new_poly)
    # figureFrame = changeFigureSystemCoordinate(newFigure, X, Y, 'toFrame')
    return newFigures


def changePointSystemCoordinates(point, X, Y, mode):
    if mode == 'toNormal':
        newX = point[0]-X/2
        newY = Y/2 - point[1]
        newPoint = [newX, newY]
        return newPoint
    else:
        newX = point[0]+X/2
        newY = Y/2 - point[1]
        newPoint = [newX, newY]
        return newPoint


def calc_coord(coords, X, Y):
    points = []
    for coordinate in coords:
        x = coordinate[0]
        y = coordinate[1]
        # print([x, y, math.sin(math.radians(45))])
        new_coord = changePointSystemCoordinates([x, y], X, Y, 'toFrame')
        points.append(new_coord)
    return points