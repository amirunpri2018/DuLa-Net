import math
import numpy as np

def coords2uv(coords):  
    #coords: 0.0 - 1.0
    coords = (coords[0] - 0.5, coords[1] - 0.5)

    uv = (coords[0] * 2 * math.pi,
            -coords[1] * math.pi)

    return uv

def uv2coords(uv):

    coordsX = uv[0] / (2 * math.pi) + 0.5
    coordsY = -uv[1] / math.pi + 0.5

    coords = (coordsX, coordsY)

    return coords

def uv2xyz(uv, N):

    x = math.cos(uv[1]) * math.sin(uv[0])
    y = math.sin(uv[1])
    z = math.cos(uv[1]) * math.cos(uv[0])
    xyz = (N * x, N * y, -N * z)

    return xyz

def xyz2uv(xyz):

    epsilon = 1e-17

    normXZ = math.sqrt( math.pow(xyz[0], 2) + math.pow(xyz[2], 2) )
    normXZ = epsilon if normXZ < epsilon else normXZ

    normXYZ = math.sqrt(math.pow(xyz[0], 2) + 
                        math.pow(xyz[1], 2) + 
                        math.pow(xyz[2], 2) )
    normXYZ = epsilon if normXYZ < epsilon else normXYZ

    v = math.asin(xyz[1] / normXYZ)
    u = math.asin(xyz[0] / normXZ)

    if xyz[2] > 0 and u > 0:
        u = math.pi - u
    elif xyz[2] > 0 and u < 0:
        u = -math.pi - u

    if xyz[0] == 0 and xyz[2] > 0:
        u = math.pi

    uv = (u, v)

    return uv

def coords2xyz(coords, N):

    uv = coords2uv(coords)
    xyz = uv2xyz(uv, N)
    
    return xyz

def xyz2coords(xyz):

    uv = xyz2uv(xyz)
    coords = uv2coords(uv)

    return coords

def pos2coords(pos, size):
    
    coords = (float(pos[0]) / size[0], float(pos[1]) / size[1])
    return coords

def coords2pos(coords, size):
    
    pos = (int(coords[0] * (size[0]-1)), 
            int(coords[1] * (size[1]-1)))
    return pos

def xyz2pos(xyz, size):

    coords = xyz2coords(xyz)
    pos = coords2pos(coords, size)
    return pos

def pos2xyz(pos, size, N):

    coords = pos2coords(pos, size)
    xyz = coords2xyz(coords, N)
    return xyz

def posTranspose(pos):

    ans = (pos[1], pos[0])
    return ans

def points2coords(points):

    ans = []
    for p in points:
        ans.append(xyz2coords(p))
    return ans

def pointsCrossPano(p1, p2):
    
    if p1[2] > 0 and p2[2] > 0:
        
        if p1[0] < 0 and p2[0] >= 0:
            return True, p1, p2
        elif p1[0] >= 0 and p2[0] < 0:
            return True, p2, p1
        else:
            return False, None, None
    else:
        return False, None, None

def cameraCoords2Vector(camPose, coords, fov):

    x_offset = -(coords[0] - 0.5) * fov[0]
    y_offset = (coords[1] - 0.5) * fov[1]

    hcam_rad = (camPose[0] + x_offset) / 180.0 * math.pi
    vcam_rad = -(camPose[1] + y_offset) / 180.0 * math.pi

    x = math.sin(hcam_rad)
    z = math.cos(hcam_rad)
    y = math.sin(vcam_rad)

    return (x, y, z)