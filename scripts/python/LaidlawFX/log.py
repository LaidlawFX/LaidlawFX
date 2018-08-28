# =============================================================================
# IMPORTS
# =============================================================================

import hou

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: node(node,level,string)
#  Raises: N/A
# Returns: N/A
#    Desc: A verbosity print function that handles ui based logging levels.
# -----------------------------------------------------------------------------      
def node(node,level,string):
    if node.parm("enableVerbosity") :
        eVil = node.evalParm("enableVerbosity")    
        if eVil >= level:
            print string
    else :
        print string

# -----------------------------------------------------------------------------
#    Name: script(level,string)
#  Raises: N/A
# Returns: N/A
#    Desc: A verbosity print function that handles script based logging levels.
#          0 = Always print.
#          1 = Print if HOUDINI_ADMIN variable is also set.
# -----------------------------------------------------------------------------      
def script(level,string):
    if hou.getenv("HOUDINI_ADMIN", False) and level >= 1:   
        print string    
    elif level == 0 :
        print string        
