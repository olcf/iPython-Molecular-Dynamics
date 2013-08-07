#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py

from optparse import OptionParser
import json
import ipython_md
import potential_function

def parse_constants(constants):
    constant_dictionary = {}
    if constants is None: return constant_dictionary
    for constant in constants:
        (key,value) = constant.split(':')
        constant_dictionary[key] = float(value)
    return constant_dictionary

def parse_command_line_options():
    usage = "usage: %prog [options] INPUT_FILE OUTPUT_FILE"
    parser = OptionParser(usage)
    parser.add_option("-p", "--potential",     dest="potential",     help="choose which potential module to use (default is 'spring')",                default="spring", type="string")
    parser.add_option("-s", "--step_size",     dest="step_size",     help="the time between each calculation (default is 0.1)",                        default=0.1,      type="float")
    parser.add_option("-o", "--output_format", dest="output_format", help="Specify either CSV or JSON for the format of OUTPUT_FILE (default is csv)", default="csv",    type="string")
    parser.add_option("-d", "--duration",      dest="duration",      help="Duration of the simulation (default is 1)",                                 default=1,        type="float")
    parser.add_option("-c", "--constant",      dest="constants",     help="use as many time as needed to specify constants as name:value (i.e -c epsilon:1.0 -c sigma:0.03)", action="append")
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("You must specify an input file and an output file")
    return [options, args]
    
def load_formatter(module_name):
    print "Loading %s output formatter..." % (module_name)
    return __import__(module_name + "-format")
         
def load_particle_data(filename):
    print "Loading particle data from %s" % (filename)
    input_file = open(filename)
    particle_data = json.load(input_file)
    input_file.close()
    return particle_data
    
def save_output(results, formatter, filename):
    print "Saving results to %s" % (filename)
    formatted_results = formatter.format(results)
    output_file = open(filename, 'w')
    output_file.write(formatted_results)
    output_file.close()
    
def main():
    (options, args) = parse_command_line_options()
    (input_file, output_file) = args
    constants = parse_constants(options.constants)
    potential = potential_function.load_potential(options.potential, constants)
    formatter_module = load_formatter(options.output_format)
    particle_data = load_particle_data(input_file)
    results = ipython_md.main(options.step_size, options.duration, potential, particle_data)
    save_output(results, formatter_module, output_file)
        
if __name__ == "__main__":
    main()