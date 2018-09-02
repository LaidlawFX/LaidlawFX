#orbolts is safe

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
#    Name: Color()
#  Raises: N/A
# Returns: None
#    Desc: Changes color of node to progressively brighten
# -----------------------------------------------------------------------------

def brighten(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        eAC     = node.evalParm("enableAutoColoring")
        if eAC == 0 :
            node.parmTuple('nodeColor').deleteAllKeyframes()
            node.parmTuple('nodeColor').set((0.0, 0.6, 1.0))
            node.setColor(hou.Color((0.0, 0.6, 1.0)))
        else:
            node.parmTuple('nodeColor').deleteAllKeyframes()
            node.parmTuple('nodeColor').set((0.0, 0.6, 1.0))
            node.setColor(hou.Color((0.0, 0.6, 1.0)))
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return


# -----------------------------------------------------------------------------
#    Name: Color(node)
#  Raises: N/A
# Returns: None
#    Desc: Enable color script, Changes the node color to a render color, if already rendered brightens it up
# -----------------------------------------------------------------------------        
        
def change(node):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        eAC     = node.evalParm("enableAutoColoring")

        nCr     = node.evalParm("nodeColorr")
        nCg     = node.evalParm("nodeColorg")
        nCb     = node.evalParm("nodeColorb")
        nCrN    = max(min(nCr+.05, 1), 0)
        nCgN    = max(min(nCg+.025, 1), 0)
        nCbN    = max(min(nCb+.05, 1), 0)

        if eAC == 1 :
            node.parmTuple('nodeColor').deleteAllKeyframes()
            node.parmTuple('nodeColor').set((nCrN, nCgN, nCbN))
            node.setColor(hou.Color((nCrN, nCgN, nCbN)))

                
        nodeNameShort = str(node).rstrip('0123456789')
        
        if nodeNameShort == 'FinalAsset' :
            node.parm('enableAutoColoring').set(0)
            node.parmTuple('nodeColor').deleteAllKeyframes()
            node.parmTuple('nodeColor').set((0.6, 0.4, 0.2))
            node.setColor(hou.Color((0.6, 0.4, 0.2)))

        nodeNameContains = str(node).lower()
            
        if "cache" in nodeNameContains :
            node.parm('enableAutoColoring').set(0)
            node.parmTuple('nodeColor').deleteAllKeyframes()
            node.parmTuple('nodeColor').set((0.6, 0.4, 0.2))
            node.setColor(hou.Color((0.6, 0.4, 0.2)))

               
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return        