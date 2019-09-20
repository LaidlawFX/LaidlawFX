# =============================================================================
# IMPORTS
# =============================================================================

import hou
from hda.vertex_animation_textures import utils

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: preset(node)
#  Raises: N/A
# Returns: None
#    Desc: Engine setting.
# -----------------------------------------------------------------------------

def preset(node,method):
    print('unity')    
    node.parm('coord_pos').deleteAllKeyframes()
    node.parm('coord_pos').set(0)
    node.parm('invert_pos').deleteAllKeyframes()
    node.parm('invert_pos').set(1)
    node.parm('coord_rot').deleteAllKeyframes()
    node.parm('coord_rot').set(11) 
    node.parm('scale_max_min').deleteAllKeyframes()
    node.parm('scale_max_min').set(1)            
    if node.parm('method') == 3 : 
        node.parm('reverse_norm').deleteAllKeyframes()
        node.parm('reverse_norm').set(1)                     
          
    
