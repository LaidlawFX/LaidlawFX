using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using UnityEditor;
using UnityEditorInternal;
using UnityEngine;
using Directory = System.IO.Directory;

internal sealed class VAT_AssetImporter : AssetPostprocessor {
    private static readonly string _basePath = "Assets/VAT";
    private static string _baseString = "_mesh_vat";
    private static string _assetName = "default";
    private static string _shaderName = "LaidlawFX/Default";
    private static string _materialName = "default_mat_vat.mat";   

    private static string MeshPath   
    {
        get
        {
            return _basePath + "/Meshes";
        }
    }
    private static string TexturePath
    {
        get
        {
            return _basePath + "/Textures";
        }
    } 
    private static string MaterialsPath
    {
        get
        {
            return _basePath + "/Materials";
        }
    }
    private static string PrefabPath
    {
        get
        {
            return _basePath + "/Prefabs";
        }
    }    
    private static List<string> baseMeshImports;

    private static Material _mainMaterial;
    private static Material _oldMaterial;    

    #region Methods

    #region Pre Processors

    void OnPreprocessTexture() {
        // Get a reference to the assetImporter which is contained in the class we've inherited from AssetPostProcessor
        TextureImporter importer = assetImporter as TextureImporter;
        if (importer == null) return;        
        string        name      = importer.assetPath.ToLower();
        if (!name.Contains("_vat")) return;

        // note: Global settings for all the platforms
        importer.textureType        = TextureImporterType.Default;
        importer.textureShape       = TextureImporterShape.Texture2D;                
        importer.sRGBTexture        = false;
        importer.alphaSource        = TextureImporterAlphaSource.FromInput;
        importer.alphaIsTransparency = false;
        importer.npotScale          = TextureImporterNPOTScale.None;
        importer.isReadable         = false;
        importer.streamingMipmaps   = false;
        importer.mipmapEnabled      = false;
        importer.wrapMode           = TextureWrapMode.Repeat;
        importer.filterMode         = FilterMode.Point;

        // Standalone
        // Construct the class that contains our importer settings, we'll re-use this class per platform by changing any fields we need changed
        // Let's start with standalone build target, "name" field determines the target platform
        var tips = new TextureImporterPlatformSettings() {
                                                             allowsAlphaSplitting = false,
                                                             androidETC2FallbackOverride = AndroidETC2FallbackOverride.Quality16Bit,
                                                             compressionQuality   = 100,
                                                             crunchedCompression  = false,
                                                             format               = importer.DoesSourceTextureHaveAlpha() ? TextureImporterFormat.RGBAHalf : TextureImporterFormat.RGBA32,
                                                             maxTextureSize       = 8192,
                                                             name                 = "Standalone",
                                                             overridden           = true,
                                                             textureCompression   = TextureImporterCompression.Uncompressed,
                                                         };
        importer.SetPlatformTextureSettings(tips);

        // At this point we don't need to declare and define a settings class, just change the fields we want changed and re-use it!
        // iPhone
        tips.name           = "iPhone";
        importer.SetPlatformTextureSettings(tips);
        // Web
        // tips.name           = "Web";
        // importer.SetPlatformTextureSettings(tips);        
        // Android
        tips.name           = "Android";
        importer.SetPlatformTextureSettings(tips);
        // WebGL - Does not handle RGBAHalf
        // tips.name           = "WebGL";
        // importer.SetPlatformTextureSettings(tips);
        // Windows Store Apps
        tips.name           = "Windows Store Apps";
        importer.SetPlatformTextureSettings(tips);  
        // PS4
        tips.name           = "PS4";
        importer.SetPlatformTextureSettings(tips); 
        // PSM
        tips.name           = "PSM";
        importer.SetPlatformTextureSettings(tips); 
        // XboxOne
        tips.name           = "XboxOne";
        importer.SetPlatformTextureSettings(tips);  
        // Nintendo 3DS
        tips.name           = "Nintendo 3DS";
        importer.SetPlatformTextureSettings(tips); 
        // tvOS
        tips.name           = "tvOS";
        importer.SetPlatformTextureSettings(tips);                                       

    }


    void OnPreprocessModel() {
        ModelImporter importer  = assetImporter as ModelImporter;
        string        name      = importer.assetPath.ToLower();
        if (!name.Contains("_vat")) return;
        string        extension = name.Substring(name.LastIndexOf(".")).ToLower();
        switch (extension) {
            case ".fbx":
                // Model - Scene
                importer.globalScale        = 1.0F;
                importer.useFileUnits       = true;
                importer.importBlendShapes  = false;
                importer.importVisibility   = false;
                importer.importCameras      = false;
                importer.importLights       = false;
                importer.preserveHierarchy  = false;
                // Model - Meshes
                importer.meshCompression    = ModelImporterMeshCompression.Off;
                importer.isReadable         = false;
                //importer.optimizeMesh       = false;
                importer.optimizeMeshPolygons = false;
                importer.optimizeMeshVertices = false;
                importer.addCollider        = false;
                // Model - Geometry
                importer.keepQuads          = false;
                importer.weldVertices       = false;
                importer.indexFormat        = ModelImporterIndexFormat.Auto;
                importer.importNormals      = ModelImporterNormals.None;
                importer.importTangents     = ModelImporterTangents.None;
                importer.swapUVChannels     = false;
                importer.generateSecondaryUV = false;
                // Rig
                importer.animationType      = ModelImporterAnimationType.None;
                // Animation
                importer.importAnimation    = false;
                importer.importConstraints  = false;
                // Materials            
                // importer.importMaterials    = true;
                importer.materialImportMode = ModelImporterMaterialImportMode.ImportViaMaterialDescription;
                importer.useSRGBMaterialColor = false;
                importer.materialLocation   = ModelImporterMaterialLocation.InPrefab;
                importer.materialName       = ModelImporterMaterialName.BasedOnMaterialName;
                importer.materialSearch     = ModelImporterMaterialSearch.Everywhere;
                importer.SearchAndRemapMaterials(ModelImporterMaterialName.BasedOnMaterialName, ModelImporterMaterialSearch.Everywhere);
                break;
            default:
                break;
        }
    }
    
    #endregion Pre Processors

    #region Post Processors 

    // Post processors get invoked after the asset is sucessfully imported, now we can edit the crated assets from our source files

    private void OnPostprocessTexture(Texture2D import) { }

    private void OnPostprocessModel(GameObject import) { }

    /// Runs after all assets are imported and creates assigned materials in prefabs
    static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets,
        string[] movedFromAssetPaths)
    {
        List<string> baseMeshImports = new List<string>();
 
        //Pull out the assets inside the proper folders
        foreach (string importedAsset in importedAssets)
        {
            if (!importedAsset.Contains(_basePath))
            {
                return;
            }
 
            //ignore the casing, in case things are typed wrong.
            //Grab only assets that have the _baseString in its name.
            Match match = Regex.Match(importedAsset, _baseString, RegexOptions.IgnoreCase);
            if (match.Success)
            {
                //Add it to our import List
                baseMeshImports.Add(importedAsset);              
            }
        }
 
        //Figure out the name of each asset and build it based on that
        foreach (var baseMaterial in baseMeshImports)
        {
            //Remove the extension from the filename so we dont have to mess with it.
            var fileName = Path.GetFileNameWithoutExtension(baseMaterial);
 
            if (fileName != null)
            {
                //Name the prefab without the _baseString so it clear what it is
                _assetName = fileName.Replace(_baseString, "");
 
                //Iterable prefab construction method
                ConstructPrefab(baseMaterial);
            }
        }
    }

    /// Initial call to construct prefab. 
    private static void ConstructPrefab(string importedFilePath)
    {
        //Load the asset from the project
        var importedFile = (GameObject) AssetDatabase.LoadAssetAtPath(importedFilePath, typeof(GameObject));
 
        //Instantiate the prefab in to the scene so we can start to work with it
        var instantiatedBaseMesh = GameObject.Instantiate(importedFile);
 
        // Rebuild the material with the textures
        CreateMaterial();

        // Grab the mesh objects and apply the new material to it.
        ApplyMaterialsToMesh(instantiatedBaseMesh);
 
        //Start putting the prefab together
        CreatePrefab(instantiatedBaseMesh);
    }


    /// Rebuilds the material on the asset.
    public static void CreateMaterial()
    {
        //clear out the main material in case it is filled in from previous import
        _mainMaterial = null;
 
        //Make sure the materials directoy exists before adding stuff to it
        if (!Directory.Exists(MaterialsPath))
        {
            Directory.CreateDirectory(MaterialsPath);
        }

        //Check all the files in the directory for the main material
        foreach(var file in Directory.GetFiles(MaterialsPath, "*.mat", SearchOption.TopDirectoryOnly))
        {  
            if (!file.Contains(_assetName)) continue;            
            if (file.Contains("sft"))
            {
                _shaderName = "LaidlawFX/Soft";
                _materialName = _assetName + "_sft_mat_vat.mat";
            } 
            else if (file.Contains("rgd"))
            {
                _shaderName = "LaidlawFX/Rigid";
                _materialName = _assetName + "_rgd_mat_vat.mat";
            }
            else if (file.Contains("fld"))
            {
                _shaderName = "LaidlawFX/Fluid";
                _materialName = _assetName + "_fld_mat_vat.mat";
            } 
            else 
            {
                _shaderName = "LaidlawFX/Sprite";
                _materialName = _assetName + "_spr_mat_vat.mat";
            } 

            //compare strings and check for the materialname in the file
            Match match = Regex.Match(file, _materialName, RegexOptions.IgnoreCase);
 
            //If the file exists, set the old material variable with the project file
            if (match.Success)
            {
                _oldMaterial = (Material)AssetDatabase.LoadAssetAtPath(file, typeof(Material));
            }
        }

        //create a new material
        var tempMaterial = new Material(Shader.Find(_shaderName));
        string tempName = "temp_mat_vat.mat";
        //save material to the project directory
        AssetDatabase.CreateAsset(tempMaterial, Path.Combine(MaterialsPath, tempName));

        //load up the the new material and store it
        _mainMaterial = (Material)AssetDatabase.LoadAssetAtPath(Path.Combine(MaterialsPath, tempName), typeof(Material));
        // copy the old material options to the new material
        _mainMaterial.CopyPropertiesFromMaterial(_oldMaterial);
        // destroy the old material
        AssetDatabase.DeleteAsset(Path.Combine(MaterialsPath, _materialName));
        // rename the new material
        AssetDatabase.RenameAsset(Path.Combine(MaterialsPath, tempName),_materialName);        

        //Grab the position texture if it exists
        Debug.Log("Warning: Textures not being applied."); 
        string texturePath = GetFilesPathNotMeta(TexturePath, _assetName + "_pos_vat").Replace("\\","/");
        Debug.Log("this is my pos texture path : " +texturePath); 
        Texture2D posTex = (Texture2D)AssetDatabase.LoadAssetAtPath(texturePath, typeof(Texture2D));
        int temp = posTex.GetInstanceID();
        Debug.Log(temp);
 
        //if (posTex != null)
        //{
        //    _mainMaterial.SetTexture("_posTex", posTex);
        //}
        _mainMaterial.SetTexture("_posTex", posTex);

 
        //Grab the rotation map path if it exists
        texturePath = GetFilesPathNotMeta(TexturePath, _assetName + "_rot_vat").Replace("\\","/");
 
        Texture2D rotTex = (Texture2D)AssetDatabase.LoadAssetAtPath(texturePath, typeof(Texture2D));
 
        if (rotTex != null)
        {
            _mainMaterial.SetTexture("_rotTex", rotTex);
        }
 
        //Grab the Scale map path if it exists
        texturePath = GetFilesPathNotMeta(TexturePath, _assetName + "_scale_vat");
 
        Texture2D scaleTex = (Texture2D)AssetDatabase.LoadAssetAtPath(texturePath, typeof(Texture2D));
 
        if (scaleTex != null)
        {
            _mainMaterial.SetTexture("_scaleTex", scaleTex);
        }

        //Grab the rotation map path if it exists
        texturePath = GetFilesPathNotMeta(TexturePath, _assetName + "_norm_vat");
 
        Texture2D normTex = (Texture2D)AssetDatabase.LoadAssetAtPath(texturePath, typeof(Texture2D));
 
        if (normTex != null)
        {
            _mainMaterial.SetTexture("_normTex", normTex);
        }
 
        //Grab the Scale map path if it exists
        texturePath = GetFilesPathNotMeta(TexturePath, _assetName + "_col_vat");
 
        Texture2D colTex = (Texture2D)AssetDatabase.LoadAssetAtPath(texturePath, typeof(Texture2D));
 
        if (colTex != null)
        {
            _mainMaterial.SetTexture("_colTex", colTex);
        }        
    }  

    // Applys the material to the mesh in the prefab
    private static void ApplyMaterialsToMesh(GameObject baseMesh)
    {
        foreach (var mesh in baseMesh.GetComponentsInChildren<Renderer>())
        {
            mesh.sharedMaterial = _mainMaterial;
        }        
    }
 
    /// Creates a prefab with materials 
    private static void CreatePrefab(GameObject assetPrefab)
    {
        Selection.activeGameObject = assetPrefab;
 
        //Set the name of the object to be the prefab name
        assetPrefab.name = _assetName;
        
        //Save\Create the prefab in the project hierarchy
        var folder = Directory.CreateDirectory(PrefabPath); 
        string prefabSavePath = string.Format("{0}/Prefabs/{1}_PF.prefab", _basePath, _assetName);
        PrefabUtility.SaveAsPrefabAsset(assetPrefab,prefabSavePath);
 
        GameObject.DestroyImmediate(assetPrefab);
    }

    // Return the raw fbx file, not a meta file
    private static string GetFilesPathNotMeta(string filePath, string searchString)
    {
        return Directory.GetFiles(filePath).FirstOrDefault(
            x => x.IndexOf(searchString, StringComparison.OrdinalIgnoreCase) >= 0 &&
                 x.IndexOf(".meta") < 0);
    }

    #endregion Post Processors

    #endregion Methods
}