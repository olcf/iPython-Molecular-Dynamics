# lennard-jones-accel module
import numpy

def required_constants():
    return ["epsilon","sigma"]

def force_on_a_due_to_b(position_of_a, position_of_b, constants):
    epsilon = constants["epsilon"]
    sigma = constants["sigma"]
    r = numpy.linalg.norm(position_of_a - position_of_b)
    return 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)