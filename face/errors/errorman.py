import errors

active_errors = []

def get_error_msg(eid):
    return errors.error_msg[eid]
    
def register_error(eid, target=None):
    active_errors.append( (eid, target) )
        
def get_errors(clear=True):
    global active_errors
    
    errors = active_errors
    if clear:
        active_errors = []
    return errors
    
def get_printable_errors(clear=True):
    return [get_error_msg(x[0]) for x in get_errors(clear)]
    
def clear_errors():
    active_errors = []