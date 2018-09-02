# =============================================================================
# IMPORTS
# =============================================================================

import os
import hou
import inspect

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
#    Name: load(node, geo, path)
#  Raises: N/A
# Returns: None
#    Desc: Loads the geo like a file sop.
# -----------------------------------------------------------------------------

def load(node, geo, path):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:   
        missingframe    = node.evalParm("missingframe")
        try:
            _geo = hou.Geometry()
            _geo.loadFromFile(path)
            geo.merge(_geo)
        except hou.OperationFailed:
            print("Could not load: " + path)
        except hou.GeometryPermissionError:
            print("Permissions Issue, are the files locked?")        
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return      
        
# -----------------------------------------------------------------------------
#    Name: write(node, geo, path)
#  Raises: N/A
# Returns: None
#    Desc: Loads the geo like a file sop.
# -----------------------------------------------------------------------------

def write(node, geo, path):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:   
        missingframe    = node.evalParm("missingframe")
        try:
            geo.saveToFile(path)
        except hou.OperationFailed:
            print("Could not write: " + path)         
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return
        
# -----------------------------------------------------------------------------
#    Name: read(node, geo, child)
#  Raises: N/A
# Returns: None
#    Desc: Read tiles
# -----------------------------------------------------------------------------

def read(node, geo, child, type):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:
        missingframe    = node.evalParm("missingframe")
        enableTile      = node.evalParm("enableTile")    
        skipInput       = node.evalParm("skipInput")
        filePath        = node.hm().path.filePath(node)
        
        dataList = []
        if skipInput or len(node.node("IN").inputs()) == 0:
            
            g_dataList = []
            if type == "cells":
                if enableTile:      
                    get_cell_num    = child.inputs()[2].geometry()
                    g_dataList      = get_cell_num.attribValue("dataList")
                    g_dataList      = [str(int(c)).zfill(5) for c in g_dataList.split(',')]
                
                try:
                    _dataList       = node.evalParm("dataList").replace(' ', '')
                    dataList        = [str(int(c)).zfill(5) for c in _dataList.split(',')]
                    dataList        += g_dataList
                    
                except ValueError:
                    
                    if not g_dataList:
                        if missingframe == 0:
                            raise hou.NodeError("Invalid "+type+" parameter")
                        else:
                            raise hou.NodeWarning("Invalid "+type+" parameter")
                    else:
                        dataList = g_dataList 
                        
            elif type == "tiles":
                get_tile_num        = child.inputs()[2].geometry()
                try:
                    g_dataList          = get_tile_num.attribValue("dataList")
                    g_dataList          = [str("x" + t.replace("_", "_y")) for t in g_dataList.split(',')]
                except:
                    print "No Data List...exiting"
                    return 
    
                if not g_dataList:
                    if missingframe == 0:
                        raise hou.NodeError("Invalid "+type+" parameter")
                    else:
                        raise hou.NodeWarning("Invalid "+type+" parameter")
                else:
                    dataList        = g_dataList
    
        else: 
            input_geo       = child.inputs()[1].geometry()
            _dataList       = input_geo.attribValue("dataList")
            if not _dataList:
                if missingframe == 0:
                    raise hou.NodeError("'dataList' detail attribute not found on input")
                else:
                    raise hou.NodeWarning("'dataList' detail attribute not found on input")
            
            if type == "cells":
                dataList    = [str(int(c)).zfill(5) for c in _dataList.split(',')]
            elif type == "tiles":
                dataList    = [str("x" + t.replace("_", "_y")) for t in _dataList.split(',')]      
        
        if not dataList:
            if missingframe == 0:
                raise hou.NodeError(type +" parameter is empty")
            else:
                raise hou.NodeWarning(type +" parameter is empty")
            
        dataList = list(set(dataList))
    
        for data in dataList:
            if type == "cells":       
                file = filePath.replace("%CELLNUM%", data)
            elif type == "tiles":
                file = filePath.replace("%TILENUM%", data)
            
            if not os.path.exists(file): continue
            if os.path.getsize(file) == 594L: continue
    
            node.hm().file.load(node, geo, file)  
            
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return      
# -----------------------------------------------------------------------------
#    Name: readPattern(node, geo, child, type)
#  Raises: N/A
# Returns: None
#    Desc: Fetch tile geos from prefix / label pattern, this is way slower than direct loading
#          as the entier cache folder must be parse to fetch valid files.
# -----------------------------------------------------------------------------

def readPattern(node, geo, child, type):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:    
        missingframe    = node.evalParm("missingframe")
        skipInput       = node.evalParm("skipInput")
        enableTile      = node.evalParm("enableTile")
        folderSubType   = node.hm().path.folderSubType(node)
        label_pattern   = node.evalParm("label")
        prefix_pattern  = node.evalParm("prefix")
        filePath        = node.hm().path.filePath(node)
        
        dataList = []
        if skipInput or len(node.node("IN").inputs()) == 0:
            
            g_dataList = []
            if type == "cells":    
                if enableTile:        
                    get_cell_num    = child.inputs()[2].geometry()
                    g_dataList      = get_cell_num.attribValue("dataList")
                    g_dataList      = [str(int(c)).zfill(5) for c in g_dataList.split(',')]
                
                try:
                    _dataList       = node.evalParm("dataList").replace(' ', '')
                    dataList        = [str(int(c)).zfill(5) for c in _dataList.split(',')]
                    dataList        += g_dataList
                    
                except ValueError:
                    if not g_list:
                        if missingframe == 0:
                            raise hou.NodeError("Invalid data parameter")
                        else:
                            raise hou.NodeWarning("Invalid data parameter")   
                    else:
                        dataList = g_dataList
    
            elif type == "tiles":    
                get_tile_num        = child.inputs()[2].geometry()
                g_dataList          = get_tile_num.attribValue("dataList")
                g_dataList          = [str("x" + t.replace("_", "_y")) for t in g_dataList.split(',')]
                
                if not g_dataList:
                    if missingframe == 0:
                        raise hou.NodeError("Invalid data parameter")
                    else:
                        raise hou.NodeWarning("Invalid data parameter")
                else:
                    dataList = g_dataList
    
        else: 
            input_geo   = child.inputs()[1].geometry()
            _dataList   = input_geo.attribValue("dataList")
            if not _dataList:
                if missingframe == 0:
                    raise hou.NodeError("'dataList' detail attribute not found on input")
                else:
                    raise hou.NodeWarning("'dataList' detail attribute not found on input")
            
            if type == "cells":                
                dataList        = [str("x" + t.replace("_", "_y")) for t in _dataList.split(',')]
            if type == "tiles": 
                dataList        = [str(int(c)).zfill(5) for c in _dataList.split(',')]            
        
        if not dataList:
            if missingframe == 0:
                if missingframe == 0:
                    raise hou.NodeError("data parameter is empty")
                else:
                    raise hou.NodeWarning("data parameter is empty")
        
        try:           
            dataList        = list(set(dataList))
            path_root       = os.path.dirname(filePath)
    
            if type == "cells":
                valid_files = [f for f in os.listdir(path_root) if \
                               f.split('_')[-1].split('.', 1)[0] in dataList]
            if type == "tiles":   
                valid_files = [f for f in os.listdir(path_root) if \
                               f.split('.')[0][-7:] in dataList]                     
                           
            for f in valid_files:
                
                # check if label matches
                if label_pattern and label_pattern != '*':
                    current = f.split(folderSubType + '_')[-1]
    
                    if type == "cells":
                        file_label  = current.split("cell")[0]
                    if type == "tiles":   
                        current = current.split('.', 1)[0]
                        file_label  = current.replace(current[-8:], '')
                    
                    # doesn't have label
                    if not file_label:
                        continue
                    
                    if not hou.patternMatch(label_pattern, file_label):
                        continue
                        
                # check if prefix matches
                if prefix_pattern and prefix_pattern != '*':
                    _p = f.split(folderSubType)[0]
                    
                    if not _p:
                        continue
                        
                    if not hou.patternMatch(prefix_pattern, _p):
                        continue
                file = path_root + '/' + f      
                node.hm().file.load(node, geo, file)
                
        except WindowsError:
            print("Path error: " + filePath)
            
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return
# -----------------------------------------------------------------------------
#    Name: readSingle(node, geo, type)
#  Raises: N/A
# Returns: None
#    Desc: Writes CSV files
# -----------------------------------------------------------------------------

def readSingle(node, geo, type):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:   
        missingframe    = node.evalParm("missingframe")
        filePath        = node.hm().path.filePath(node)
        
        if "%TILENUM%" in filePath:
            tilex = node.parm("tilex").evalAsString().zfill(2)
            tiley = node.parm("tiley").evalAsString().zfill(2)
            filePath = filePath.replace("%TILENUM%", "x" + tilex + "_y" + tiley)
    
        node.hm().file.load(node, geo, filePath)    
        
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return
# -----------------------------------------------------------------------------
#    Name: readSinglePattern(node, geo, type)
#  Raises: N/A
# Returns: None
#    Desc: Writes CSV files
# -----------------------------------------------------------------------------

def readSinglePattern(node, geo, type):
    nodePath    = node.path()
    function    = inspect.stack()[0][3]
    try:    
        filePath        = node.hm().path.filePath(node)
        label_pattern   = node.evalParm("label")
        prefix_pattern  = node.evalParm("prefix")
        folderSubType   = node.hm().path.folderSubType(node)
        data_level      = node.hm().path.folderDataType(node)
        
        tile = "_x{}_y{}".format(str(node.evalParm("tilex")).zfill(2),
                                 str(node.evalParm("tiley")).zfill(2))
        
        root, f = os.path.split(filePath)
        
        if data_level == "tile":
            files = [n for n in os.listdir(root) if tile in n]
        else:
            files = os.listdir(root)
        
        for f in files:
            
            # check if label matches
            if label_pattern and label_pattern != '*':
                current = f.split(folderSubType + '_')[-1]
                
                file_pattern = current.split(tile)[0]
                if not hou.patternMatch(label_pattern, file_pattern):
                    continue
                    
            # check if prefix matches
            if prefix_pattern and prefix_pattern != '*':
                _p = f.split(folderSubType)[0]
                if not _p:
                    continue
                if not hou.patternMatch(prefix_pattern, _p):
                    continue
    
            file = path_root + '/' + f      
            node.hm().file.load(node, geo, file) 
            
    except (KeyboardInterrupt, SystemExit):
        print "Interrupt requested of "+function+" for "+nodePath+"...exiting"
        return            