# particle_storage module

def store_single_particle(position, velocity, acceleration):
    return {"position": position, "velocity": velocity, "acceleration": acceleration}

def log_particle_data(time, current_particle_data, historical_particle_data):
    historical_particle_data.append({"time": time, "particles": current_particle_data})
    
def get_current_particle_data(particle_data):
    return particle_data[-1]["particles"]

def new_particle_log():
    return []