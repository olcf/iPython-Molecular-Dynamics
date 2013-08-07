# ipython_md module
import numpy
import dynamics
import particle_storage
    
def extract_particle_masses(particle_data):
    masses = []
    for particle in particle_data:
        masses.append(particle["mass"])
    return masses

def transform_initial_data_to_numerical_arrays(particles):
    num_particles = len(particles)
    for i in range(0,num_particles):
        for key in ["position","velocity"]:
            particles[i][key] = numpy.array(particles[i][key])
    
def update_positions(stepsize, particles):
    temporary_particles = []
    for particle in particles:       
        tmp_particle = dynamics.update_position(stepsize, particle)
        temporary_particles.append(tmp_particle)
    return temporary_particles
    
def update_velocities(stepsize, particles):
    new_particles = []
    for particle in particles:
        new_particle = dynamics.update_velocity(stepsize, particle)
        new_particles.append(new_particle)
    return new_particles
    
def update_accelerations(particles, potential, masses):
    force_matrix = dynamics.calculate_force_matrix(particles, potential)
    forces = dynamics.sum_forces(force_matrix)
    accels = dynamics.calculate_accelerations(masses, forces)
    tmp_particles = []
    num_particles = len(particles)
    for i in range(0, num_particles):
        position = particles[i]["position"]
        velocity = particles[i]["velocity"]
        accel    = accels[i]
        tmp_particle = particle_storage.store_single_particle(position, velocity, accel)
        tmp_particles.append(tmp_particle)
    return tmp_particles
       
def main(stepsize, duration, potential, initial_particle_data):
    transform_initial_data_to_numerical_arrays(initial_particle_data["particles"])
    masses = extract_particle_masses(initial_particle_data["particles"])
    initial_particle_data["particles"] = update_accelerations(initial_particle_data["particles"], potential, masses)
    current_time = 0.0
    particle_data_log = particle_storage.new_particle_log()
    particle_storage.log_particle_data(current_time, initial_particle_data["particles"], particle_data_log)
    while(current_time < duration):
        current_particles = particle_storage.get_current_particle_data(particle_data_log)
        updated_particles = update_positions(stepsize, current_particles)
        updated_particles = update_accelerations(updated_particles, potential, masses)
        updated_particles = update_velocities(stepsize, updated_particles)
        current_time += stepsize
        particle_storage.log_particle_data(current_time, updated_particles, particle_data_log)
    return particle_data_log
