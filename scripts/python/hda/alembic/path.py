# =============================================================================
# IMPORTS
# =============================================================================

import os
import hou

# -----------------------------------------------------------------------------
#    Name: alembic_frame()
#  Raises: N/A
# Returns: None
#    Desc: Sketchfab FBX sequence
#          '$HIP/ifds/$HIPNAME.$F.ifd'
# -----------------------------------------------------------------------------

def alembic_frame():
    frame = str(hou.intFrame()).zfill(5)      
    return frame

# -----------------------------------------------------------------------------
#    Name: sketchfab_png(node)
#  Raises: N/A
# Returns: None
#    Desc: Sketchfab FBX sequence
#          '$HIP/ifds/$HIPNAME.$F.ifd'
# -----------------------------------------------------------------------------

def alembic_texture(node):
    path_abc    = node.evalParm('fileName')    
    frame       = alembic_frame()    
    filelist    =['tex.',frame,'.png']
    filename    =''.join(filelist)          
    path_file   = os.path.abspath(os.path.splitext(path_abc)[0] +'_ABC_TEXTURE/'+filename).replace("\\","/")    
    return path_file