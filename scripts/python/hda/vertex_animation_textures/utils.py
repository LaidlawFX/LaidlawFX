# =============================================================================
# IMPORTS
# =============================================================================

import hou
import os
import json
import imp
import pkgutil
import importlib

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: data(node)
#  Raises: N/A
# Returns: None
#    Desc: Updates material values.
# -----------------------------------------------------------------------------

def data(node):
    #print 'Updating Json'
    path            = os.path.abspath(node.evalParm('path_data'))
    directory       = os.path.dirname(path)
    #remove file if exist
    try:
        os.remove(path)
    except OSError:
        pass       
    #create directory if it does not exist    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    engine       = str(node.evalParm('engine'))
    method       = node.evalParm('method')
    component    = node.evalParm('_component')        
    _numOfFrames = str(node.evalParm('num_frames'))
    _speed       = str(node.evalParm('speed'))
    _posMax      = str(node.evalParm('max_min_pos1'))
    _posMin      = str(node.evalParm('max_min_pos2'))
    _scaleMax    = str(node.evalParm('max_min_scale1'))
    _scaleMin    = str(node.evalParm('max_min_scale2'))
    _pivMax      = str(node.evalParm('max_min_piv1'))
    _pivMin      = str(node.evalParm('max_min_piv2'))
    _packNorm    = str(node.evalParm('pack_norm'))
    _packPscale  = str(node.evalParm('pack_pscale'))
    _normData    = str(node.evalParm('normalize_data'))
    _width       = str(node.evalParm('width_height1'))
    _height      = str(node.evalParm('width_height2'))        
       
    data = {}  
    data[component] = []  
    data[component].append({ 
        '_numOfFrames'  : _numOfFrames,
        '_speed'        : _speed,
        '_posMax'       : _posMax,
        '_posMin'       : _posMin,
        '_scaleMax'     : _scaleMax,
        '_scaleMin'     : _scaleMin,
        '_pivMax'       : _pivMax,
        '_pivMin'       : _pivMin,
        '_packNorm'     : _packNorm,
        '_packPscale'   : _packPscale,
        '_normData'     : _normData,
        '_width'        : _width,
        '_height'       : _height         
    })
    with open(path, 'w') as f:  
        json.dump(data, f, indent=4, sort_keys=True)
                  
# -----------------------------------------------------------------------------
#    Name: _project()
#  Raises: N/A
# Returns: None
#    Desc: Defines what the component should be called.
# -----------------------------------------------------------------------------

def _project(node):
    project           = node.evalParm("project")
    project_enable    = node.evalParm("enable_project")
    
    if project_enable == 1 and project != "" :
        project       = project           
    else :
        project       = hou.hscriptExpression('$JOB')  
    
    return project

# -----------------------------------------------------------------------------
#    Name: primcount(node)
#  Raises: N/A
# Returns: None
#    Desc: Detects the prim count based on the current frame.
# -----------------------------------------------------------------------------

def primcount(node):
    polyNode    = hou.node("objects/data/TO_Mesh")
    geo         = polyNode.geometry()
    count       = geo.countPrimType('Poly')

    if count != 0:
        node.parm('target_polycount').deleteAllKeyframes()
        node.parm('target_polycount').set(count)

# -----------------------------------------------------------------------------
#    Name: _depth(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if shader exist and creates it otherwise.
# -----------------------------------------------------------------------------

def _depth(node):
    #print node.path()
    depth       = node.evalParm('depth')
    usebwpoints = node.evalParm('usebwpoints')
    
    ntype = 7
    stype = 'float32'
    if (depth == 0 ) and usebwpoints == 0 : #or depth == 'int8'
        ntype = 0
        stype = 'int8'
    if (depth == 0 ) and usebwpoints == 1 : #or depth == 'int8'
        ntype = 1
        stype = 'int8bw'
    if (depth == 1 ) and usebwpoints == 0 : #or depth == 'int16'        
        ntype = 2
        stype = 'int16'
    if (depth == 1 ) and usebwpoints == 1 : #or depth == 'int16'
        ntype = 3
        stype = 'int16bw'
    if (depth == 2 ) and usebwpoints == 0 : #or depth == 'int32'     
        ntype = 4
        stype = 'int32'
    if (depth == 2 ) and usebwpoints == 1 : #or depth == 'int32'      
        ntype = 5
        stype = 'int32bw'
    if (depth == 3 ): #or depth == 'float16'       
        ntype = 6
        stype = 'float16'
    if (depth == 4 ): #or depth == 'float32'       
        ntype = 7
        stype = 'float32'
    
    return ntype, stype                              

# -----------------------------------------------------------------------------
#    Name: _depth(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if shader exist and creates it otherwise.
# -----------------------------------------------------------------------------

def _depth_uv(node):
    #print node.path()
    depth       = node.evalParm('depth_uv')
    
    ntype = 6
    stype = 'float16'
    if (depth == 0 ) : #or depth == 'int8'
        ntype = 0
        stype = 'int8'
    if (depth == 1 ) : #or depth == 'int16'        
        ntype = 2
        stype = 'int16'
    if (depth == 2 ) : #or depth == 'int32'     
        ntype = 4
        stype = 'int32'
    if (depth == 3 ): #or depth == 'float16'       
        ntype = 6
        stype = 'float16'
    if (depth == 4 ): #or depth == 'float32'       
        ntype = 7
        stype = 'float32'
    
    return ntype, stype  

# -----------------------------------------------------------------------------
#    Name: shader(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if shader exist and creates it otherwise.
# -----------------------------------------------------------------------------

def shader(node):
    path_shader = os.path.abspath(node.evalParm('path_shader'))
    if not os.path.isfile(path_shader) :
        engine = node.evalParm('engine') 
        method = node.evalParm('method')
        if   method == 0:
            smethod = 'soft'
        elif method == 1:
            smethod = 'rigid'   
        elif method == 2:
            smethod = 'fluid' 
        elif method == 3:
            smethod = 'sprite'
        elif method == 4:
            smethod = 'volumetric'             
        #parm = smethod +"_shader_"+str(engine)
        #node.parm(parm).revertToDefaults()
        #shader = node.evalParm(parm)
        curdir      =os.path.dirname(os.path.realpath(__file__))
        path_source =os.path.join(curdir,'engines',engine,smethod +'.shader')  

        with open(path_source, 'r') as file:
            data = file.read()  

        directory = os.path.dirname(path_shader)
        if not os.path.exists(directory):
            os.makedirs(directory)   
        with open(path_shader,'w+') as f:
            f.write(data)            

# -----------------------------------------------------------------------------
#    Name: mat_check(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if material exist and creates it otherwise.
# -----------------------------------------------------------------------------

def mat_check(node):
    path_mat = os.path.abspath(node.evalParm('path_mat'))
    if not os.path.isfile(path_mat) :
        engine = node.evalParm('engine') 
        method = node.evalParm('method')
        if   method == 0:
            smethod = 'soft'
        elif method == 1:
            smethod = 'rigid'   
        elif method == 2:
            smethod = 'fluid' 
        elif method == 3:
            smethod = 'sprite'
        elif method == 4:
            smethod = 'volumetric'            
        #parm = smethod +"_mat_"+str(engine)
        #node.parm(parm).revertToDefaults()
        #mat = node.evalParm(parm)
        curdir      =os.path.dirname(os.path.realpath(__file__))
        path_source =os.path.join(curdir,'engines',engine,smethod +'.mat')  

        with open(path_source, 'r') as file:
            data = file.read()          

        directory = os.path.dirname(path_mat)
        if not os.path.exists(directory):
            os.makedirs(directory)   
        with open(path_mat,'w+') as f:
            f.write(data)
    
    component   = str(node.evalParm('_component')) + '_mat'
    componentPath = '/mat/'+ component
    matNode     = hou.node(componentPath)
    if not matNode:
        matNode = hou.node('/mat').createNode('materialbuilder', component)
        matNode.moveToGoodPosition()
        matNode.setColor(hou.Color( (0.0, 0.6, 1.0) ) )   


# -----------------------------------------------------------------------------
#    Name: MakeList(node)
#  Raises: N/A
# Returns: None
#    Desc: Search directory for rendered folders
# -----------------------------------------------------------------------------

def list_engines(node):
    try:
        curdir      =os.path.dirname(os.path.realpath(__file__))
        engdir      =os.path.join(curdir,'engines')          
        dirList = [filename for filename in os.listdir(engdir) if os.path.isdir(os.path.join(engdir,filename))]
        dirs        = []
        for dirName in dirList:
            dirs += [dirName, dirName]
        
        return dirs
    except :
        return ["MissingEnginesInScripts", "MissingEnginesInScripts"]  

# -----------------------------------------------------------------------------
#    Name: main(node)
#  Raises: N/A
# Returns: None
#    Desc: Performs the presets for each engine.
# -----------------------------------------------------------------------------

def preset(node):
    engine = node.evalParm('engine')
    method = node.evalParm('method')   
    
    reset(node)

    module = 'hda.vertex_animation_texture.engines.'
    module += engine
    module += '.preset'
    preset_loader = pkgutil.find_loader(module)
    found = preset_loader is not None
    if found :
        #print module
        preset = importlib.import_module(module)
        preset.preset(node,method)


# -----------------------------------------------------------------------------
#    Name: reset(node)
#  Raises: N/A
# Returns: None
#    Desc: Reset all parameters
# -----------------------------------------------------------------------------

def reset(node):
    node.parm('num_frames').revertToDefaults()
    node.parm('speed').revertToDefaults()    
    node.parm('max_min_pos1').revertToDefaults() 
    node.parm('max_min_pos2').revertToDefaults()
    node.parm('max_min_piv1').revertToDefaults() 
    node.parm('max_min_piv2').revertToDefaults()     
    node.parm('max_min_scale1').revertToDefaults() 
    node.parm('max_min_scale2').revertToDefaults()
    node.parm('width_height1').revertToDefaults() 
    node.parm('width_height2').revertToDefaults()     
    node.parm('normalize_data').revertToDefaults() 
    node.parm('enable_geo').revertToDefaults() 
    node.parm('path_geo').revertToDefaults()
    node.parm('enable_pos').revertToDefaults() 
    node.parm('path_pos').revertToDefaults() 
    node.parm('enable_rot').revertToDefaults() 
    node.parm('path_rot').revertToDefaults()
    node.parm('enable_scale').revertToDefaults() 
    node.parm('path_scale').revertToDefaults()     
    node.parm('enable_norm').revertToDefaults() 
    node.parm('path_norm').revertToDefaults() 
    node.parm('enable_col').revertToDefaults() 
    node.parm('path_col').revertToDefaults()
    node.parm('update_mat').revertToDefaults() 
    node.parm('path_mat').revertToDefaults()      
    node.parm('create_shader').revertToDefaults() 
    node.parm('path_shader').revertToDefaults()
    node.parm('reverse_norm').revertToDefaults()     
    node.parm('convertcolorspace').revertToDefaults()
    node.parm('depth').revertToDefaults()     
    node.parm('pack_norm').revertToDefaults()
    node.parm('pack_pscale').revertToDefaults()     
    node.parm('coord_pos').revertToDefaults()
    node.parm('invert_pos').revertToDefaults()
    node.parm('coord_rot').revertToDefaults() 
    node.parm('coord_col').revertToDefaults() 
    node.parm('invert_col').revertToDefaults() 
    node.parm('target_polycount').revertToDefaults() 
    node.parm('target_texture_size').revertToDefaults() 
    node.parm('scale').revertToDefaults()
    node.parm('shop_materialpath').revertToDefaults()

# -----------------------------------------------------------------------------
#    Name: mat_update(node)
#  Raises: N/A
# Returns: None
#    Desc: Updates material values.
# -----------------------------------------------------------------------------

def mat_update(node):
    #print 'Updating Material'
    path = os.path.abspath(node.evalParm('path_mat'))  
    if os.path.isfile(path) :
        engine       = str(node.evalParm('engine'))
        method       = node.evalParm('method')
        _numOfFrames = str(node.evalParm('num_frames'))
        _speed       = str(node.evalParm('speed'))
        _posMax      = str(node.evalParm('max_min_pos1'))
        _posMin      = str(node.evalParm('max_min_pos2'))
        _scaleMax    = str(node.evalParm('max_min_scale1'))
        _scaleMin    = str(node.evalParm('max_min_scale2'))
        _pivMax      = str(node.evalParm('max_min_piv1'))
        _pivMin      = str(node.evalParm('max_min_piv2'))
        _packNorm    = str(node.evalParm('pack_norm'))
        _packPscale  = str(node.evalParm('pack_pscale'))
        _normData    = str(node.evalParm('normalize_data'))
        _width       = str(node.evalParm('width_height1'))
        _height      = str(node.evalParm('width_height2'))        
        
        numOfFrames  = -1
        speed        = -1
        posMax       = -1
        posMin       = -1
        scaleMax     = -1
        scaleMin     = -1
        pivMax       = -1
        pivMin       = -1
        packNorm     = -1
        packPscale   = -1
        normData     = -1
        width        = -1
        height       = -1        
        
        with open(path) as f:
            for num, line in enumerate(f, 1):
                if "_numOfFrames" in line:
                    numOfFrames = num
                if "_speed"     in line:
                    speed       = num
                if "_posMax"    in line:
                    posMax      = num
                if "_posMin"    in line:
                    posMin      = num
                if "_scaleMax"  in line:
                    scaleMax    = num
                if "_scaleMin"  in line:
                    scaleMin    = num
                if "_pivMax"    in line:
                    pivMax      = num
                if "_pivMin"    in line:
                    pivMin      = num
                if "_packNorm"  in line:
                    packNorm    = num
                if "_packPscale" in line:
                    packPscale  = num 
                if "_normData"  in line:
                    normData    = num
                if "_width"    in line:
                    width       = num
                if "_height"    in line:
                    height      = num                    

        list = open(path).readlines()
        if "_numOfFrames" != -1 :
            list[numOfFrames-1] = '    - _numOfFrames: '+_numOfFrames+'\n'
        if "_speed"       != -1 :    
            list[speed-1]       = '    - _speed: '      +_speed+'\n'
        if "_posMax"      != -1 :    
            list[posMax-1]      = '    - _posMax: '     +_posMax+'\n'
        if "_posMin"      != -1 :    
            list[posMin-1]      = '    - _posMin: '     +_posMin+'\n'
        if "_scaleMax"    != -1 :   
            list[scaleMax-1]    = '    - _scaleMax: '   +_scaleMax+'\n'
        if "_scaleMin"    != -1 :  
            list[scaleMin-1]    = '    - _scaleMin: '   +_scaleMin+'\n'
        if "_pivMax"      != -1 :   
            list[pivMax-1]      = '    - _pivMax: '     +_pivMax+'\n'
        if "_pivMin"      != -1 :  
            list[pivMin-1]      = '    - _pivMin: '     +_pivMin+'\n'
        if "_packNorm"    != -1 :  
            list[packNorm-1]    = '    - _packNorm: '   +_packNorm+'\n'
        if "_packPscale"  != -1 :    
            list[packPscale-1]  = '    - _packPscale: ' +_packPscale+'\n'
        if "_normData"    != -1 :    
            list[normData-1]    = '    - _normData: '   +_normData+'\n'
        if "_width"      != -1 :   
            list[width-1]       = '    - _width: '      +_width+'\n'
        if "_height"      != -1 :  
            list[height-1]      = '    - _height: '     +_height+'\n'            
        open(path,'w').write(''.join(list))       

# -----------------------------------------------------------------------------
#    Name: path_cop_bc_uv(node)
#  Raises: N/A
# Returns: None
#    Desc: Performs the presets for each engine.
# -----------------------------------------------------------------------------

# Has multiple node outputs need to rework this logic
def path_cop_bc_uv(node):
    bc = node.evalParm('bcChannelSplit')
    if bc == 0 :
        path = "../../textures/UV/XYZW"
    elif bc == 1 :
        path = "../../textures/UV/XYZW"
        path = "../../textures/UV/W"
    elif bc == 2 :
        path = "../../textures/UV/XYZW"
        path = "../../textures/UV/W"        
    elif bc == 3 :
        path = "../../textures/UV/XY"
        path = "../../textures/UV/ZW" 
    elif bc == 4 :
        path = "../../textures/UV/X"
        path = "../../textures/UV/Y"
        path = "../../textures/UV/Z"
        path = "../../textures/UV/W"                       
    return path      

# -----------------------------------------------------------------------------
#    Name: path_cop_bc_uv(node)
#  Raises: N/A
# Returns: None
#    Desc: Performs the presets for each engine.
# -----------------------------------------------------------------------------

def channel_comp(node):
    name        = node.name()
    parent      = node.parent().name()
    try :
        coppath     = hou.node("../../textures/"+parent+"/"+name).path()
    except :
        coppath     = "refresh node"

    path        = node.evalParm('path')
    os.path.normpath(path)
    filename, file_extension = os.path.splitext(path)
    filelist    =[filename, '_', name, file_extension]    
    path        =''.join(filelist)  
    copoutput   = filename + name + file_extension
                       
    return coppath, copoutput

# -----------------------------------------------------------------------------
#    Name: _pscale(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def minmax_pscale(node):
    try:
        #Brightest pixel represents the max bounds for scale.
        scale_max = hou.node("../textures/normalize_pscale/max").getPixelByUV(plane="C",u=0,v=0, component="r")
        #Darkest pixel represents the min bounds for position.
        scale_min = hou.node("../textures/normalize_pscale/min").getPixelByUV(plane="C",u=0,v=0, component="r")

        node.parm("max_min_scale1").set(str(float(int(scale_max[0]*100000))/100000))
        node.parm("max_min_scale2").set(str(float(int(scale_min[0]*100000))/100000))
    except :
        return    

# -----------------------------------------------------------------------------
#    Name: _scale(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def minmax_scale(node):
    try:
        #Brightest pixel represents the max bounds for scale.
        scale_max = hou.node("../textures/normalize_scale/max").getPixelByUV(plane="C",u=0,v=0, component="r")
        #Darkest pixel represents the min bounds for position.
        scale_min = hou.node("../textures/normalize_scale/min").getPixelByUV(plane="C",u=0,v=0, component="r")


        node.parm("max_min_scale1").set(str(float(int(scale_max[0]*100000))/100000))
        node.parm("max_min_scale2").set(str(float(int(scale_min[0]*100000))/100000))
    except :
        return  



# -----------------------------------------------------------------------------
#    Name: _pscale(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def minmax_pos_single(node):
    try:
        #Unity engine conversion
        engine  = node.evalParm('engine')
        scale   = 1/node.evalParm('scale')

        node_bounds    = hou.node("../objects/data/OUT_min_max_bounds")
        geo     = node_bounds.geometry()

        bbox    = geo.boundingBox()

        min_vec = bbox.minvec()
        min_pos = min(min_vec)

        max_vec = bbox.maxvec()
        max_pos = max(max_vec)

        if engine == 'unity' :
            node.parm("max_min_pos1").set(str(float(int(max_pos*100000))/100000*scale))
            node.parm("max_min_pos2").set(str(float(int(min_pos*100000))/100000*scale))
        else:
            node.parm("max_min_pos1").set(str(float(int(max_pos*100000))/100000))    
            node.parm("max_min_pos2").set(str(float(int(min_pos*100000))/100000))
    except :
        return 


# -----------------------------------------------------------------------------
#    Name: _pscale(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def minmax_pos_multi(node):
    try:
        #Unity engine conversion
        engine  = node.evalParm('engine')
        scale   = 1/node.evalParm('scale')

        #Brightest pixel represents the max bounds for position.
        position_max = hou.node("../textures/normalize_position/max").getPixelByUV(plane="C",u=0,v=0, component="r")
        #print position_max
        #Darkest pixel represents the min bounds for position.
        position_min = hou.node("../textures/normalize_position/min").getPixelByUV(plane="C",u=0,v=0, component="r")
        #print position_min

        if engine == 'unity' :
            node.parm("max_min_pos1").set(str(float(int(position_max[0]*100000))/100000*scale))
            node.parm("max_min_pos2").set(str(float(int(position_min[0]*100000))/100000*scale))
        else:
            node.parm("max_min_pos1").set(str(float(int(position_max[0]*100000))/100000))    
            node.parm("max_min_pos2").set(str(float(int(position_min[0]*100000))/100000))
    except :
        return 


# -----------------------------------------------------------------------------
#    Name: _pscale(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def minmax_pivot(node):
    try:
        #Unity engine conversion
        engine  = node.evalParm('engine')
        scale   = 1/node.evalParm('scale')

        #Pivot geo
        node_bounds = hou.node("../objects/data/OUT_min_max_bounds")
        geo  = node_bounds.geometry()

        #Represents the max bounds for pivot via the pivot.
        pivot_max = geo.attribValue("pivot_max")

        #Represents the min bounds for pivot via the pivot.
        pivot_min  = geo.attribValue("pivot_min")


        if engine == 'unity' :
            node.parm("max_min_piv1").set(str(float(int(pivot_max*100000))/100000*scale))    
            node.parm("max_min_piv2").set(str(float(int(pivot_min*100000))/100000*scale))
        else:
            node.parm("max_min_piv1").set(str(float(int(pivot_max*100000))/100000))    
            node.parm("max_min_piv2").set(str(float(int(pivot_min*100000))/100000))
    except :
        return 


# -----------------------------------------------------------------------------
#    Name: _pscale(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def minmax_frames(node):
    try:
        #Set frame range value.
        node.parm('f1').deleteAllKeyframes()
        node.parm('f2').deleteAllKeyframes()
        f1  = node.evalParm('f1')
        f2  = node.evalParm('f2')

        num_frames = abs(f2-f1)
        node.parm('num_frames').deleteAllKeyframes()
        node.parm('num_frames').set(num_frames)

        speed = hou.fps()/num_frames
        node.parm('speed').deleteAllKeyframes()
        node.parm('speed').set(speed)
    except :
        return 


# -----------------------------------------------------------------------------
#    Name: _debug_refresh(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def debug_refresh(node):
    try:
        hou.node('../objects/debug/MESH').parm('reload').pressButton()
        hou.hscript("texcache -c")
    except :
        return 

