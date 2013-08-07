# potential_function class and module
import sys

def validate_constants(potential_module, constants):
    valid = True
    for constant in potential_module.required_constants():
        valid &= constants.has_key(constant)
    return valid
    
def load_potential(module_name, constants):
    print "Loading %s potential..." % (module_name)
    module =  __import__(module_name + "-potential")
    valid = validate_constants(module, constants)
    if (not valid): 
        print "You must specify values for the following constants:"
        print module.required_constants()
        sys.exit(1)
    return Wrapper(module, constants)

class Wrapper:
    def __init__(self, module, constants):
        self.module = module
        self.constants = constants
        
    def force_on_a_due_to_b(self,a,b):
        return self.module.force_on_a_due_to_b(a,b,self.constants)