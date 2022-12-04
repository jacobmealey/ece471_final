#!/usr/bin/python3
import math
import numpy as np

# Spherical coordinates:
# rho is the distance from the origin (think radius)
# theta is the angle the rho vector forms with the x axis; 0 <= theta < 2pi
# phi is the angle the rho vector forms with the z axis; 0 <= phi < pi

def sph_to_xyz(rho, theta, phi):
    x = rho*math.sin(phi*(math.pi/180))*math.cos(theta*(math.pi/180))
    y = rho*math.sin(phi*(math.pi/180))*math.sin(theta*(math.pi/180))
    z = rho*math.cos(phi*(math.pi/180))

    return x, y, z

# Give a file name and spherical coords data
def write_xyz(fn, data):

    for i in range(data.shape[0]):
        data[i, :] = sph_to_xyz(*data[i, :])

    # xyz format expects space delimiting
    np.savetxt(fn, data, delimiter=" ")

if __name__ == "__main__":
    data = np.loadtxt("test.csv", delimiter=",")

    write_xyz("test.xyz", data)
