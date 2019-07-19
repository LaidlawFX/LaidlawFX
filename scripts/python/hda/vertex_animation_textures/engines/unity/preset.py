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
    node.parm('path_geo').deleteAllKeyframes()
    node.parm('path_geo').set('`chs(\"_project\")`/meshes/`chs(\"_component\")`_mesh.fbx')
    node.parm('path_pos').deleteAllKeyframes()
    node.parm('path_pos').set('`chs("_project")`/textures/`chs(\"_component\")`_pos.tiff')
    node.parm('path_rot').deleteAllKeyframes()
    node.parm('path_rot').set('`chs("_project")`/textures/`chs(\"_component\")`_rot.tiff')
    node.parm('path_scale').deleteAllKeyframes()
    node.parm('path_scale').set('`chs("_project")`/textures/`chs(\"_component\")`_scale.tiff')    
    node.parm('path_norm').deleteAllKeyframes()
    node.parm('path_norm').set('`chs("_project")`/textures/`chs(\"_component\")`_norm.tiff')
    node.parm('path_col').deleteAllKeyframes()
    node.parm('path_col').set('`chs("_project")`/textures/`chs(\"_component\")`_col.tiff')
    node.parm('path_uv').deleteAllKeyframes()
    node.parm('path_uv').set('`chs("_project")`/textures/`chs(\"_component\")`_uv.tiff')    
    node.parm('path_mat').deleteAllKeyframes()
    node.parm('path_mat').set('`chs("_project")`/materials/`chs(\"_component\")`_mat.mat')     
    node.parm('convertcolorspace').deleteAllKeyframes()
    node.parm('convertcolorspace').set(0)
    node.parm('depth').deleteAllKeyframes()
    node.parm('depth').set("int16")
    node.parm('pack_pscale').deleteAllKeyframes()
    node.parm('pack_pscale').set(1)
    node.parm('pack_norm').deleteAllKeyframes()
    node.parm('pack_norm').set(1)    
    node.parm('coord_pos').deleteAllKeyframes()
    node.parm('coord_pos').set(0)
    node.parm('invert_pos').deleteAllKeyframes()
    node.parm('invert_pos').set(1)
    node.parm('coord_rot').deleteAllKeyframes()
    node.parm('coord_rot').set(11)     
    if method == 0 :
        node.parm('path_shader').deleteAllKeyframes()
        node.parm('path_shader').set('`chs("_project")`/shaders/vertex_soft.shader')         
    elif method == 1 :
        node.parm('path_shader').deleteAllKeyframes()
        node.parm('path_shader').set('`chs("_project")`/shaders/vertex_rigid.shader')         
    elif method == 2 :
        node.parm('path_shader').deleteAllKeyframes()
        node.parm('path_shader').set('`chs("_project")`/shaders/vertex_fluid.shader')
        utils.primcount(node)
        if node.parm('enable_polyreduce') :     
	        node.parm('target_texture_size').deleteAllKeyframes()
	        node.parm('target_texture_size').setExpression('ch("target_polycount")*3')
    elif method == 3 : 
        node.parm('path_shader').deleteAllKeyframes()
        node.parm('path_shader').set('`chs("_project")`/shaders/vertex_sprite.shader')
        node.parm('reverse_norm').deleteAllKeyframes()
        node.parm('reverse_norm').set(1)                     
       
    utils.mat_check(node) 
    utils.shader(node)     
    
