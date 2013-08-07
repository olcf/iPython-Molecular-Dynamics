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
            
# As given in http://en.wikipedia.org/wiki/Verlet_integration#Velocity_Verlet
def velocity_verlet(stepsize, potential, position, velocity, acceleration):
    a_plus_one = potential.calculate_acceleration(x_plus_one, other_positions)
    v_plus_one = v_plus_one_half + 0.5 * a_plus_one * stepsize
    return store_single_particle(x_plus_one, v_plus_one, a_plus_one)

def apply_next_timestep(stepsize, potential, particles):
    updated_particles = []
    for particle in particles:
        position = particle["position"]
        velocity = particle["velocity"]
        acceleration = particle["acceleration"]
        updated_particles.append(velocity_verlet(stepsize, potential, position, velocity, acceleration))
    return updated_particles

def embed_initial_accelerations(particle_data, potential, masses):
    accelerations = dynamics.generate_accelerations(particle_data, potential, masses)
    num_particles = len(particle_data)
    for i in range(0,num_particles):
        particle_data[i]["acceleration"] = accelerations[i]
    
def main(stepsize, duration, potential, initial_particle_data):
    transform_initial_data_to_numerical_arrays(initial_particle_data["particles"])
    masses = extract_particle_masses(initial_particle_data["particles"])
    embed_initial_accelerations(initial_particle_data["particles"], potential, masses)
    current_time = 0.0
    particle_data_log = particle_storage.new_particle_log()
    particle_storage.log_particle_data(current_time,initial_particle_data["particles"],particle_data_log)
    while(current_time < duration):
        current_particles = particle_storage.get_current_particle_data(particle_data_log)
        updated_particles = apply_next_timestep(stepsize, potential, current_particles)
        current_time += stepsize
        particle_storage.log_particle_data(current_time, updated_particles, particle_data_log)
    return particle_data_log