import errors

active_errors = []
active_messages = []

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

## Messages that are not errors.

def register_message(message, target=None, status=None):
    active_messages.append( (message, target, status) )
    
def get_messages(clear=True):
    global active_messages
    
    msgs = active_messages
    if clear:
        active_messages = []
    return msgs
    
def get_printable_messages(clear=True):
    return [get_messages(x[0]) for x in get_messages(clear)]
    