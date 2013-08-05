# csv-format module

def format_header(num_particles):
    csv_header = ["time"]
    for i in range(1,num_particles+1):
        csv_header.append("x%d" % i)
        csv_header.append("y%d" % i)
        csv_header.append("z%d" % i)
    return ",".join(csv_header)

def format_row(snapshot):
    csv_row = ["%f" % snapshot["time"]]
    for particle in snapshot["particles"]:
        for position in particle["position"]:
            csv_row.append("%f" % position)
    return ",".join(csv_row)

def format(particle_data):
    num_particles = len(particle_data[0]["particles"])
    csv_content = [format_header(num_particles)]
    for snapshot in particle_data:
        csv_content.append(format_row(snapshot))
    return "\n".join(csv_content)