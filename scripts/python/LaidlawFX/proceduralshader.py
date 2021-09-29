#orbolts safe

# =============================================================================
# IMPORTS
# =============================================================================

import hou
import inspect
import exceptions

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: set_path(node)
#  Raises: N/A
# Returns: None
#    Desc: Set the procedural shader path to the object cached from this node
# -----------------------------------------------------------------------------

def set_path(node):
    nodePath    = node.path()
    function = inspect.stack()[0][3]
    try:

        pnode       = node.parent()
        pnodePath   = str(pnode.path())
        nodeName    = str(node)
        pnodeName   = str(pnode)    
        shaderPathGeo     = nodeName  + "/DelayedLoad/Geometry"
        shaderPathAlembic = nodeName  + "/DelayedLoad/Alembic"
        eT                = node.evalParm("eT")
        eVil              = node.evalParm("enableVerbosity")
        if eVil >= 3 :
            print("Parent Node: " + pnodeName) 
            print("Parent Path: " + pnodePath)             
 
        if eT == 0 :
            pnode.parm('shop_geometrypath').deleteAllKeyframes()
            pnode.parm('shop_geometrypath').set(shaderPathGeo)
            if eVil >= 1 :
                print("Setting Procedural Path on " + pnodePath)
                print("Path Set to " + shaderPathGeo)
        elif eT == 2 :
            pnode.parm('shop_geometrypath').deleteAllKeyframes()
            pnode.parm('shop_geometrypath').set(shaderPathAlembic)        
            if eVil >= 1 :
                print("Setting Procedural Path on " + pnodePath)
                print("Path Set to " + shaderPathAlembic)        
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return