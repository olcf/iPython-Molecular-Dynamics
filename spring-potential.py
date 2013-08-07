# spring-accel module
import numpy

def required_constants():
    return ["spring_coefficient","equilibrium_length"]

def force_on_a_due_to_b(position_of_a, position_of_b, constants):
    k = constants["spring_coefficient"]
    eqlen = constants["equilibrium_length"]
    return -k * (numpy.linalg.norm(position_of_a - position_of_b) - eqlen)