import collections
import random

Hex = collections.namedtuple("Hex", ["x", "y", "z"])
HEX_DELTAS = [Hex(1, 0, -1), Hex(1, -1, 0), Hex(0, -1, 1), Hex(-1, 0, 1), Hex(-1, 1, 0), Hex(0, 1, -1)]

def hex_add(hex1, hex2):
    return Hex(hex1.x + hex2.x, hex1.y + hex2.y, hex1.z + hex2.z)

def hex_subtract(hex1, hex2):
    return Hex(hex1.x - hex2.x, hex1.y - hex2.y, hex1.z - hex2.z)

def hex_length(hex):
    return (abs(hex.x) + abs(hex.y) + abs(hex.z)) // 2

def hex_distance(hex1, hex2):
    return hex_length(hex_subtract(hex1, hex2))

def hex_direction(direction):
    return HEX_DELTAS[direction]

def hex_neighbor(hex_, direction):
    return hex_add(hex_, hex_direction(direction))

def hex_range(center, distance):
    d = distance
    hexes = set()
    for x in range(-d, d+1):
        for y in range(-d, d+1):
            for z in range(-d, d+1):
                if x + y + z == 0:
                    hex_ = Hex(x, y, z)
                    hexes.update({hex_add(hex_, center)})
    return hexes

