# =============================================================================
# IMPORTS
# =============================================================================

import hou
import os
import re
import math
import json
import imp
import pkgutil
import importlib
from LaidlawFX import path as pth

# =============================================================================
# FUNCTIONS
# =============================================================================

# Path Functions

# -----------------------------------------------------------------------------
#    Name: project()
#  Raises: N/A
# Returns: None
#    Desc: The main path of the project
# -----------------------------------------------------------------------------

def project(node):
    project           = node.evalParm("project")
    project_enable    = node.evalParm("enable_project")
    
    if project_enable == 1 and project != "" :
        project       = project           
    else :
        project       = hou.hscriptExpression('$JOB')  
    
    os.path.normpath(project)
    return project

# -----------------------------------------------------------------------------
#    Name: path_util(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for Initial Geometry  
#          `chs("_project")`/Meshes/`chs("_component")`_mesh.fbx
# -----------------------------------------------------------------------------

def path_util(node,name,folder,ext,nameopt=None,component=None):
    path_var        = "path_"+name
    path            = node.evalParm(path_var)
    enable_var      = "enable_"+name
    path_enable     = node.evalParm(enable_var)  

    if path_enable  == 1 and path != "" :
        path        = path           
    else :
        frame_tex           = node.evalParm('frame_tex')
        method              = node.evalParm('method')

        if nameopt :
            name_ext = nameopt
        else :
            name_ext = name

        if not component :
            component = pth.component(node)  


        
        if ext is 'geometry' :            
            ext  = node.evalParm("ext_geometry")
            if ext == "" :
                ext = '.fbx'

        filelist    =['/',component,'_',name_ext,'_vat',ext]         

        if ext is 'texture' :
            ext  = node.evalParm("ext_texture")
            if ext == "" :
                ext = '.exr'
            filelist    =['/',component,'_',name_ext,'_vat',ext]   
            if frame_tex == 1 and method == 2 :
                frame          = '.'+str(hou.intFrame()).zfill(5) 
                folder = "Resources/StreamingAssets/"+component
                filelist    =['/',name_ext,frame,ext]     


        dirlist     =[project(node),folder]
           
        path        = pth.path_create(dirlist,filelist).replace("\\",'/')         
    
    os.path.normpath(path)    
    return path 

# -----------------------------------------------------------------------------
#    Name: path_atlas(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for Position  
#          `chs("_project")`/Textures/`chs("_component")`_pos.exr
# -----------------------------------------------------------------------------

def path_atlas(node):         
    ext = 'texture'   
    path = path_util(node,"data","Data",ext,"dta")  
    return path   

# -----------------------------------------------------------------------------
#    Name: path_geo(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for Initial Geometry  
#          `chs("_project")`/Meshes/`chs("_component")`_mesh.fbx
# -----------------------------------------------------------------------------

def path_geo(node):
    ext = 'geometry'   
    path = path_util(node,"geo","Meshes",ext,"mesh")  
    return path              

# -----------------------------------------------------------------------------
#    Name: path_geo_ext(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for Initial Geometry  
#          `chs("_project")`/Meshes/`chs("_component")`_mesh.fbx
# -----------------------------------------------------------------------------

def path_geo_ext(node):
    filename, file_extension = os.path.splitext(path_geo(node))
    file_extension.lower()
    value = 0
    if file_extension == '.fbx':
        value = 1  
    return value  

# -----------------------------------------------------------------------------
#    Name: path_pos(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for Position  
#          `chs("_project")`/Textures/`chs("_component")`_pos.exr
# -----------------------------------------------------------------------------

def path_pos(node):
    ext = 'texture'     
    path = path_util(node,"pos","Textures",ext)  
    return path    

# -----------------------------------------------------------------------------
#    Name: path_norm(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for Normals
#          `chs("_project")`/Textures/`chs("_component")`_norm.exr
# -----------------------------------------------------------------------------

def path_norm(node):
    ext = 'texture'  
    path = path_util(node,"norm","Textures",ext,"nml")  
    return path   

# -----------------------------------------------------------------------------
#    Name: path_col(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for color
#          `chs("_project")`/Textures/`chs("_component")`_col.exr
# -----------------------------------------------------------------------------

def path_col(node):
    ext = 'texture'    
    path = path_util(node,"col","Textures",ext)  
    return path    

# -----------------------------------------------------------------------------
#    Name: path_rot(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for orient
#          `chs("_project")`/Textures/`chs("_component")`_rot.exr
# -----------------------------------------------------------------------------

def path_rot(node):
    ext = 'texture'     
    path = path_util(node,"rot","Textures",ext)  
    return path  

# -----------------------------------------------------------------------------
#    Name: path_scale(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for scale
#          `chs("_project")`/Textures/`chs("_component")`_scale.exr
# -----------------------------------------------------------------------------

def path_scale(node):
    ext = 'texture'    
    path = path_util(node,"scale","Textures",ext,"scl")  
    return path      
# -----------------------------------------------------------------------------
#    Name: path_uv(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for UVs
#          `chs("_project")`/Textures/`chs("_component")`_uv.exr
# -----------------------------------------------------------------------------

def path_uv(node):
    ext = 'texture'     
    path = path_util(node,"uv","Textures",ext,"uvw")  
    return path      

# -----------------------------------------------------------------------------
#    Name: path_mat(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for Materials in Unity 
#          `chs("_project")`/Materials/`chs("_component")`_mat.mat
# -----------------------------------------------------------------------------

def path_mat(node):
    ext = '.mat' 
    path = path_util(node,"mat","Materials",ext)  
    return path     

# -----------------------------------------------------------------------------
#    Name: path_data(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for text data 
#          `chs("_project")`/Materials/`chs("_component")`_data.json
# -----------------------------------------------------------------------------

def path_data(node):
    ext = '.json'
    path = path_util(node,"data","Materials",ext)  
    return path      

# -----------------------------------------------------------------------------
#    Name: path_shader(node)
#  Raises: N/A
# Returns: None
#    Desc: Path for shader
#          `chs("_project")`/Shaders/`chs("_component")`vertex.shader
# -----------------------------------------------------------------------------

def path_shader(node):
    smethod = method_str(node)   
    ext = '.shader'
    path = path_util(node,"shader","Shaders",ext,"vertex",smethod)  
    return path  

# -----------------------------------------------------------------------------
#    Name: channel_comp(node)
#  Raises: N/A
# Returns: None
#    Desc: Adds a suffix when splitting the channels between multiple textures
# -----------------------------------------------------------------------------

def channel_comp(node):
    name        = node.name()
    parent      = node.parent().name()
    try :
        coppath     = node.node("../../textures/"+parent+"/"+name).path()
    except :
        coppath     = "refresh node"

    path        = node.evalParm('path')
    os.path.normpath(path)
    filename, file_extension = os.path.splitext(path)
    filelist    =[filename, '_', name, file_extension]    
    copoutput   =''.join(filelist) 
    os.path.normpath(copoutput).replace('//', '/') 
                       
    return coppath, copoutput


# -----------------------------------------------------------------------------
#    Name: oppath_geo(node)
#  Raises: N/A
# Returns: None
#    Desc: Path to Geometry export object
#          `ifs(ch("../enable_name")==1,"/export/"+chs("../name"),"/export/MESH")`
#          `opfullpath("..") + chsop("export_node")`
# -----------------------------------------------------------------------------

def oppath_geo(node):
    name        = 'MESH'
    enable      = node.evalParm("enable_name")
    name_parm   = node.evalParm("name")
    if (enable == 1) and (name_parm != '') :
        name = re.sub('[. ]','',name_parm)
        
    node_path               = node.path()
    node_name               = node_path.replace('/', '')
    temp_subnet             = '_temp_vat_'+node_name
    export_node             = '/obj/'+temp_subnet     
    oppath                  = export_node +'/' + name
 
    return oppath, name, temp_subnet 

# -----------------------------------------------------------------------------
#    Name: oppath_geo_create(node)
#  Raises: N/A
# Returns: None
#    Desc: Create Mesh node on export
# -----------------------------------------------------------------------------
#

def oppath_geo_create(node):
    oppath, name, temp_subnet = oppath_geo(node) 

    # delete temporary export subnet if it exist
    export_node             = hou.node('/obj/'+temp_subnet)
    if export_node != None :
        export_node.destroy()

    # Create parent subnet folder in a directory no one will ever name
    parent_node             = hou.node('/obj').createNode('subnet', temp_subnet)
    parent_node.setColor(hou.Color( (0.0, 0.6, 1.0) ) )    
    parent_node.moveToGoodPosition()

    # Create geometry node we will export      
    fbx_node                = parent_node.createNode('geo', name)          
    fbx_node.setColor(hou.Color( (0.0, 0.6, 1.0) ) )
    fbx_node.moveToGoodPosition()

    fbx_node.parm('tx').set(node.evalParm("tx")) 
    fbx_node.parm('ty').set(node.evalParm("ty")) 
    fbx_node.parm('tz').set(node.evalParm("tz"))
    fbx_node.parm('sx').set(node.evalParm("sx")) 
    fbx_node.parm('sy').set(node.evalParm("sy")) 
    fbx_node.parm('sz').set(node.evalParm("sz")) 
    fbx_node.parm('rx').set(node.evalParm("rx")) 
    fbx_node.parm('ry').set(node.evalParm("ry")) 
    fbx_node.parm('rz').set(node.evalParm("rz")) 
    fbx_node.parm('px').set(node.evalParm("px")) 
    fbx_node.parm('py').set(node.evalParm("py")) 
    fbx_node.parm('pz').set(node.evalParm("pz"))         

    # import the mesh data 
    fbx_node_import         = fbx_node.createNode('object_merge','Import') 
    fbx_node_import.setColor(hou.Color( (0.0, 0.6, 1.0) ) )    
    fbx_node_import.moveToGoodPosition()

    fbx_node_import         = fbx_node.node('Import')
    fbx_node_import.parm('xformtype').set('none')
    mesh_node               = node.node('data/OUT_Mesh')
    fbx_node_import.parm('objpath1').set(mesh_node.path())           

    matnet_node             = parent_node.createNode('matnet', 'material')          
    matnet_node.setColor(hou.Color( (0.0, 0.6, 1.0) ) )
    matnet_node.moveToGoodPosition()

    mat_name                = pth.component(node) + '_mat_vat'
    mat_node                = matnet_node.createNode('LaidlawFX::vertex_animation_textures::1.0', mat_name)          
    mat_node.setColor(hou.Color( (0.0, 0.6, 1.0) ) )
    mat_node.moveToGoodPosition()
    mat_node.parm('_posTex').set(path_pos(node))
    mat_node.parm('_rotTex').set(path_rot(node))
    mat_node.parm('_scaleTex').set(path_scale(node))
    mat_node.parm('_colTex').set(path_col(node))
    mat_node.parm('_normTex').set(path_norm(node))
    node_bounds   = node.node("data/OUT_max_min")
    geo           = node_bounds.geometry()        
    mat_node.parm('_numOfFrames').set(geo.attribValue("frange"))
    mat_node.parm('_speed').set(geo.attribValue("speed"))
    mat_node.parm('_posMax').set(geo.attribValue("bbx_max"))
    mat_node.parm('_posMin').set(geo.attribValue("bbx_min"))
    mat_node.parm('_scaleMax').set(geo.attribValue("scale_max"))
    mat_node.parm('_scaleMin').set(geo.attribValue("scale_min"))
    mat_node.parm('_pivMax').set(geo.attribValue("pivot_max"))
    mat_node.parm('_pivMin').set(geo.attribValue("pivot_min"))
    mat_node.parm('_doubleTex').set(node.evalParm('bitDepthPack'))
    mat_node.parm('_padPowTwo').set(node.evalParm('padpowtwo'))
    mat_node.parm('_textureSizeX').set(geo.attribValue("img_size1"))
    mat_node.parm('_textureSizeY').set(geo.attribValue("img_size2"))
    mat_node.parm('_paddedSizeX').set(geo.attribValue("pad_size1"))
    mat_node.parm('_paddedSizeY').set(geo.attribValue("pad_size2"))        
    mat_node.parm('_packNorm').set(node.evalParm('pack_norm'))
    mat_node.parm('_packPscale').set(node.evalParm('pack_pscale'))
    mat_node.parm('_normData').set(node.evalParm('normalize_data'))
    mat_node.parm('_width').set(node.evalParm('width_height1'))
    mat_node.parm('_height').set(node.evalParm('width_height2'))          

    mat_path                = node.evalParm("shop_materialpath")
    if mat_path :
        mat_node            = node.node(mat_path)
        
    fbx_node.parm('shop_materialpath').set(mat_node.path()) 

# -----------------------------------------------------------------------------
#    Name: oppath_geo_delete(node)
#  Raises: N/A
# Returns: None
#    Desc: Delete the parent node
# -----------------------------------------------------------------------------

def oppath_geo_delete(node):
    oppath, name, temp_subnet = oppath_geo(node) 

    enable      = node.evalParm("enable_geo_debug")
    if (enable == 0) :
        # delete temporary export subnet if it exist
        export_node             = hou.node('/obj/'+temp_subnet)
        if export_node != None :
            export_node.destroy()


# File Checks/Updates/Creation

# -----------------------------------------------------------------------------
#    Name: shader(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if shader exist and creates it otherwise.
# -----------------------------------------------------------------------------

def shader(node):
    path = path_shader(node)
    if not os.path.isfile(path) :
        engine = node.evalParm('engine') 
        smethod = method_str(node)           
        curdir      =os.path.dirname(os.path.realpath(__file__))
        path_source =os.path.join(curdir,'engines',engine,smethod +'.shader')  

        with open(path_source, 'r') as file:
            data = file.read()  

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)   
        with open(path,'w+') as f:
            f.write(data)            

# -----------------------------------------------------------------------------
#    Name: method_int(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if material exist and creates it otherwise.
# -----------------------------------------------------------------------------

def method_str(node):
    method = node.evalParm('method')
    if   method == 0:
        smethod = 'soft'
    elif method == 1:
        smethod = 'rigid'   
    elif method == 2:
        smethod = 'fluid' 
    elif method == 3:
        smethod = 'sprite'  
    return smethod

# -----------------------------------------------------------------------------
#    Name: unity_assetimporter(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if material exist and creates it otherwise.
# -----------------------------------------------------------------------------

def unity_assetimporter(node):
    engine = node.evalParm('engine') 
    smethod = method_str(node)        
    curdir      =os.path.dirname(os.path.realpath(__file__))
    path_source =os.path.join(curdir,'engines',engine,'VAT_AssetImporter.cs')  

    dirlist     =[project(node),'Editor']
    filelist    =['/','VAT_AssetImporter.cs']     
         
    path        = pth.path_create(dirlist,filelist).replace("\\",'/')  
    if not os.path.isfile(path) :
        with open(path_source, 'r') as file:
            data = file.read()  

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)   
        with open(path,'w+') as f:
            f.write(data)


# -----------------------------------------------------------------------------
#    Name: mat_check(node)
#  Raises: N/A
# Returns: None
#    Desc: Checks if material exist and creates it otherwise.
# -----------------------------------------------------------------------------

def mat_check(node):
    path = path_mat(node)
    if not os.path.isfile(path) :
        engine = node.evalParm('engine') 
        smethod = method_str(node)        
        curdir      =os.path.dirname(os.path.realpath(__file__))
        path_source =os.path.join(curdir,'engines',engine,smethod +'.mat')  

        with open(path_source, 'r') as file:
            data = file.read()          

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)   
        with open(path,'w+') as f:
            f.write(data)
        mat_update(node)
    
# -----------------------------------------------------------------------------
#    Name: mat_update(node)
#  Raises: N/A
# Returns: None
#    Desc: Updates material values.
# -----------------------------------------------------------------------------

def mat_update(node):
    #print 'Updating Material'
    path = path_mat(node) 
    # print path
    if not os.path.isfile(path) :
        mat_check(node)
    else :
        node_bounds   = node.node("data/OUT_max_min")
        geo           = node_bounds.geometry()        
        _numOfFrames = str(geo.attribValue("frange"))
        _speed       = str(geo.attribValue("speed"))
        _posMax      = str(geo.attribValue("bbx_max"))
        _posMin      = str(geo.attribValue("bbx_min"))
        _scaleMax    = str(geo.attribValue("scale_max"))
        _scaleMin    = str(geo.attribValue("scale_min"))
        _pivMax      = str(geo.attribValue("pivot_max"))
        _pivMin      = str(geo.attribValue("pivot_min"))
        _doubleTex   = str(node.evalParm('bitDepthPack'))
        _padPowTwo   = str(node.evalParm('padpowtwo'))
        _textureSizeX= str(geo.attribValue("img_size1"))
        _textureSizeY= str(geo.attribValue("img_size2"))
        _paddedSizeX = str(geo.attribValue("pad_size1"))
        _paddedSizeY = str(geo.attribValue("pad_size2"))        
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
        doubleTex    = -1
        padPowTwo    = -1
        textureSizeX = -1
        textureSizeY = -1
        paddedSizeX  = -1
        paddedSizeY  = -1        
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
                if "_doubleTex" in line:
                    doubleTex   = num
                if "_padPowTwo" in line:
                    padPowTwo   = num
                if "_textureSizeX" in line:
                    textureSizeX= num
                if "_textureSizeY" in line:
                    textureSizeY= num
                if "_paddedSizeX" in line:
                    paddedSizeX = num
                if "_paddedSizeY" in line:
                    paddedSizeY = num                    
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
        if "_doubleTex"    != -1 :  
            list[doubleTex-1]    = '    - _doubleTex: '   +_doubleTex+'\n'
        if "_padPowTwo"    != -1 :  
            list[padPowTwo-1]    = '    - _padPowTwo: '   +_padPowTwo+'\n'
        if "_textureSizeX"    != -1 :  
            list[textureSizeX-1] = '    - _textureSizeX: '   +_textureSizeX+'\n'
        if "_textureSizeY"    != -1 :  
            list[textureSizeY-1] = '    - _textureSizeY: '   +_textureSizeY+'\n'
        if "_paddedSizeX"    != -1 :  
            list[paddedSizeX-1] = '    - _paddedSizeX: '   +_paddedSizeX+'\n'
        if "_paddedSizeY"    != -1 :  
            list[paddedSizeY-1] = '    - _paddedSizeY: '   +_paddedSizeY+'\n'            
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
#    Name: data(node)
#  Raises: N/A
# Returns: None
#    Desc: Updates material values.
# -----------------------------------------------------------------------------

def data(node):
    #print 'Updating Json'
    path            = path_data(node)
    directory       = os.path.dirname(path)
    #remove file if exist
    try:
        os.remove(path)
    except OSError:
        pass       
    #create directory if it does not exist    
    if not os.path.exists(directory):
        os.makedirs(directory)
    component    = pth.component(node) 
    node_bounds   = node.node("data/OUT_max_min")
    geo           = node_bounds.geometry()        
    _numOfFrames = str(geo.attribValue("frange"))
    _speed       = str(geo.attribValue("speed"))
    _posMax      = str(geo.attribValue("bbx_max"))
    _posMin      = str(geo.attribValue("bbx_min"))
    _scaleMax    = str(geo.attribValue("scale_max"))
    _scaleMin    = str(geo.attribValue("scale_min"))
    _pivMax      = str(geo.attribValue("pivot_max"))
    _pivMin      = str(geo.attribValue("pivot_min"))           
    _packNorm    = str(node.evalParm('pack_norm'))
    _doubleTex   = str(node.evalParm('bitDepthPack'))
    _padPowTwo   = str(node.evalParm('padpowtwo'))
    _textureSizeX= str(geo.attribValue("img_size1"))
    _textureSizeY= str(geo.attribValue("img_size2"))
    _paddedSizeX = str(geo.attribValue("pad_size1"))
    _paddedSizeY = str(geo.attribValue("pad_size2"))    
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
        '_doubleTex'    : _doubleTex,
        '_padPowTwo'    : _padPowTwo,
        '_textureSizeX' : _textureSizeX,
        '_textureSizeY' : _textureSizeY,
        '_paddedSizeX'  : _paddedSizeX,
        '_paddedSizeY'  : _paddedSizeY,        
        '_packPscale'   : _packPscale,
        '_normData'     : _normData,
        '_width'        : _width,
        '_height'       : _height         
    })
    try:
        #print path
        with open(path, 'w') as f:  
            json.dump(data, f, indent=4, sort_keys=True)
    except :
        print "Did not write realtime data."
        return   

# UI Presets

# -----------------------------------------------------------------------------
#    Name: preset(node)
#  Raises: N/A
# Returns: None
#    Desc: Performs the presets for each engine.
# -----------------------------------------------------------------------------

def preset(node):
    engine = node.evalParm('engine')
    method = node.evalParm('method')   
    
    reset(node)

    module = 'hda.vertex_animation_textures.engines.'
    module += engine
    module += '.preset'
    module_check = pkgutil.find_loader(module)
    if module_check is not None :
        #print module
        preset = importlib.import_module(module)
        preset.preset(node,method)

# -----------------------------------------------------------------------------
#    Name: preset_path(node)
#  Raises: N/A
# Returns: None
#    Desc: Performs the presets for each engine.
# -----------------------------------------------------------------------------

def preset_path(node):
    engine = node.evalParm('engine')
    method = node.evalParm('method')   

    module = 'hda.vertex_animation_textures.engines.'
    module += engine
    module += '.preset'
    module_check = pkgutil.find_loader(module)
    path =  None
    if module_check is not None :
        #print module
        preset = importlib.import_module(module)
        path = os.path.abspath(preset.__file__)
    print path
    return path

# -----------------------------------------------------------------------------
#    Name: reset(node)
#  Raises: N/A
# Returns: None
#    Desc: Reset all parameters
# -----------------------------------------------------------------------------

def reset(node):     
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
    node.parm('enable_mat').revertToDefaults()
    node.parm('path_mat').revertToDefaults()
    node.parm('enable_shader').revertToDefaults() 
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
    node.parm('scale_max_min').revertToDefaults()

# UI Control Options
                
# -----------------------------------------------------------------------------
#    Name: primcount(node)
#  Raises: N/A
# Returns: None
#    Desc: Detects the prim count based on the current frame.
# -----------------------------------------------------------------------------

def primcount(node):
    polyNode    = node.node("data/IN")
    print polyNode.path()
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
#    Name: _debug_refresh(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def debug_refresh(node):
    try:
        node.node('debug/MESH').parm('reload').pressButton()
        hou.hscript("texcache -c")
    except :
        return 

# -----------------------------------------------------------------------------
#    Name: frame(node)
#  Raises: N/A
# Returns: None
#    Desc: Sets value
# -----------------------------------------------------------------------------

def frame(node):   
    f1                  = node.evalParm('f1')
    f2                  = node.evalParm('f2')
    timeshift           = node.evalParm('timeshift')
    frange              = abs(f2-f1)
    frange_seq          = frange
    frame_tex           = node.evalParm('frame_tex')
    atlas_tex           = node.evalParm('atlas_tex')    
    method              = node.evalParm('method')
    speed               = float(node.evalParm('fps'))/float(frange)

    f2_tex              = f1
    if frame_tex == 1 and method == 2 :
        f2_tex          = f2 
    if (atlas_tex == 1) and (frame_tex == 1) and (method == 2) :
        frange_seq      = 1 
    if (timeshift == 1) and (frame_tex == 1) and (method == 2) :
        f1          = 0
        f2          = frange
        f2_tex      = frange                

    return f1, f2, frange, f2_tex, speed, frange_seq

