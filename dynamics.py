# dynamics module
import numpy
import particle_storage
                                        
def calculate_force_matrix(particles, potential):
    num_particles = len(particles)
    force_matrix = numpy.zeroes((num_particles,num_particles))
    for i in range(0,num_particles):
        for j in range(0,num_particles):
            if (i < j):
                a = particles[i]["position"]
                b = particles[j]["position"]
                magnitude = potential.force_on_a_due_to_b(a,b)
                direction = (a - b) / numpy.linalg.norm(a - b)
                force_matrix[i][j] = magnitude * direction
            elif (i == j): #Included for clarity
                force_matrix[i][j] = numpy.zeros(3)
            elif (i > j):
                force_matrix[i][j] = -force_matrix[j][i]
    return force_matrix

def sum_forces(force_matrix):
    particle_forces = []
    num_particles = len(force_matrix)
    for i in range(0, num_particles):
        total_force = numpy.zeros(3)
        for j in range(0, num_particles):
            total_force += force_matrix[i][j]
        particle_forces.append(total_force)
    return particle_forces

def calculate_accelerations(particle_masses, particle_forces):
    num_particles = len(particle_masses)
    accelerations = []
    for i in range(0,num_particles):
        acceleration = particle_forces[i] / particle_masses[i]
        accelerations.append(acceleration)
    return accelerations
                        
def generate_accelerations(particles, potential, masses):
    force_matrix = calculate_force_matrix(particles, potential)
    forces = sum_forces(force_matrix)
    return calculate_accelerations(masses, forces)

def update_position(stepsize, potential, position, velocity, acceleration):
    """ Part 1 of the Velocity Verlet Algorithm """
    v_plus_one_half = velocity + 0.5 * acceleration * stepsize
    x_plus_one = position + v_plus_one_half * stepsize
    return [x_plus_one, v_plus_one_half]
    
def update_positions(stepsize, potential, particles):
    temporary_particles = []
    for particle in particles:
        position = particle["position"]
        velocity = particle["velocity"]
        acceleration = particle["acceleration"]
        (position, velocity) = update_position(stepsize, potential, position, velocity, acceleration)
        temporary_particles.append(particle_storage.store_single_particle(position, velocity, acceleration))
        