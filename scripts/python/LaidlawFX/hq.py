# =============================================================================
# IMPORTS
# =============================================================================

import hou
import os
import getpass
import xmlrpclib

# =============================================================================
# GLOBAL VARIABLES
# =============================================================================


# -----------------------------------------------------------------------------
#    Name: hq_hfs(node)
#  Raises: N/A
# Returns: verSubmit, valid
#    Desc: Query the version of Houdini on the farm to present to the user.
#          Prevent submission if version matching does not work.    
# -----------------------------------------------------------------------------

def hq_hfs(node):   
    server          = node.evalParm("hq_server")
    # Connect to the HQueue server.
    hq_server       = xmlrpclib.ServerProxy("http://"+server)
    verFarm         = hq_server.getVersion().split('.')
    hfs             = r"C:/PROGRA~1/SIDEEF~1/Houdini "
    verLocal        = hou.applicationVersion()

    verMatch        = node.evalParm("verMatch")
    
    verSubmit       = ""    
    valid           = 0    
    #Exact version match required (major=, minor=, build=)     
    if ( verMatch == "exact" and 
        verFarm == verLocal ):
        valid       = 1
        verSubmit   = hfs + '.'.join(verFarm)         
    #Match minor, allow later build version (major=, minor=, build+)        
    elif ( verMatch == "minorMatchLaterBuild" and 
        verFarm[0] == verLocal[0] and 
        verFarm[1] == verLocal[1] and
        verFarm[2] >= verLocal[2]
        ):
        valid       = 1
        verSubmit   = hfs + verLocal[0]+'.'+verLocal[1]+'.'+verFarm[2]
    #Match minor, allow any build version (major=, minor=, build~)    
    elif ( verMatch == "minorMatchFuzzyBuild" and
        verFarm[0] == verLocal[0] and 
        verFarm[1] == verLocal[1] 
        ):
        valid       = 1
        verSubmit   = hfs + verLocal[0]+'.'+verLocal[1]+'.'+verFarm[2]        
    #Match major, allow later minor version (major=, minor+)
    elif ( verMatch == "majorMatchLaterMinor" and
        verFarm[0] == verLocal[0] and 
        verFarm[1] >= verLocal[1]
        ):
        valid       = 1
        verSubmit   = hfs + verLocal[0]+'.'+verFarm[1]+'.'+verFarm[2]        
    #Match major, allow any minor version (major=, minor~)
    elif ( verMatch == "majorMatchFuzzyMinor" and
        verFarm[0] == verLocal[0]
        ):
        valid       = 1
        verSubmit   = hfs + verLocal[0]+'.'+verFarm[1]+'.'+verFarm[2]        
    #Best effort to match (Later versions preferred)
    elif ( verMatch == "bestEffort" and
        verFarm[0] >= verLocal[0] and 
        verFarm[1] >= verLocal[1] and
        verFarm[2] >= verLocal[2]
        ):
        valid       = 1
        verSubmit   = hfs + verFarm[0]+'.'+verFarm[1]+'.'+verFarm[2]        
    return verSubmit, valid

