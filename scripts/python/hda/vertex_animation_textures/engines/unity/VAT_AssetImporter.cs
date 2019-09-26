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
    /// <summary>
    /// For our example character, limit the path to only be conan
    /// </summary>
    private static readonly string _basePath = "Assets";

    /// <summary>
    /// returns the texture path relative to the base path
    /// </summary>
    private static string MeshPath   
    {
        get
        {
            return _basePath + "/Meshes";
        }
    }
    /// <summary>
    /// name of our base file to work on
    /// </summary>
    private static string _baseString = "_mesh_vat";

    /// <summary>
    /// the name of prefab being saved
    /// </summary>
    private static string _assetName;
     
    /// <summary>
    /// returns the texture path relative to the base path
    /// </summary>
    private static string TexturePath
    {
        get
        {
            return _basePath + "/Textures";
        }
    } 
    /// <summary>
    /// Returns the materials path relative to the base path
    /// </summary>
    private static string MaterialsPath
    {
        get
        {
            return _basePath + "/Materials";
        }
    }
    /// <summary>
    /// Returns the materials path relative to the base path
    /// </summary>
    private static string PrefabPath
    {
        get
        {
            return _basePath + "/Prefabs";
        }
    }    
    // private static List<string> _materialFiles;
    private static List<string> baseMeshImports;

    /// <summary>
    /// returns the shader path relative to the base path
    /// </summary>
    // private static string ShaderPath = "Assets/Shaders";
 
    /// <summary>
    /// Main material asset on disk
    /// </summary>
    private static Material _mainMaterial;
    private static Material _oldMaterial;    
    private static Material _newMaterial;
 
    /// <summary>
    /// Names for texture maps
    /// </summary>
    // private static string posTex = "_pos_vat";
    // private static string rotTex = "_rot_vat";
    // private static string scaleTex = "_scale_vat";
    // private static string normTex = "_norm_vat";
    // private static string colTex = "_col_vat";

    #region Methods

    #region Pre Processors

    void OnPreprocessTexture() {
       // Extract the filename from the path
        var fileNameIndex = assetPath.LastIndexOf('/');
        var fileName      = assetPath.Substring(fileNameIndex + 1);

        // If the file name doesn't start with "tex" (e.g. texGrass.png) we won't change how it's imported, return
        // note: You can add as many such elements and change all the below settings based on these strings. Use StartsWith, EndsWith, Contains etc.
        //if (!fileName.EndsWith("_vat")) return;

        // Get a reference to the assetImporter which is contained in the class we've inherited from AssetPostProcessor
        var importer = assetImporter as TextureImporter;
        if (importer == null) return;

        // note: Some global settings I use for all the platforms, feel free to move these into settings below if they differ per-platform for you
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
        // WebGL - Does not hangle RGBAHalf
        // tips.name           = "WebGL";
        // importer.SetPlatformTextureSettings(tips);
        // Android
        tips.name           = "Windows Store Apps";
        importer.SetPlatformTextureSettings(tips);  
        // Android
        tips.name           = "PS4";
        importer.SetPlatformTextureSettings(tips); 
        // Android
        tips.name           = "PSM";
        importer.SetPlatformTextureSettings(tips); 
        // Android
        tips.name           = "XboxOne";
        importer.SetPlatformTextureSettings(tips);  
        // Android
        tips.name           = "Nintendo 3DS";
        importer.SetPlatformTextureSettings(tips); 
        // Android
        tips.name           = "tvOS";
        importer.SetPlatformTextureSettings(tips);                                       

    }


    void OnPreprocessModel() {
        var fileNameIndex = assetPath.LastIndexOf('/');
        var fileName      = assetPath.Substring(fileNameIndex + 1);

        // If the file name doesn't start with "tex" (e.g. texGrass.png) we won't change how it's imported, return
        // note: You can add as many such elements and change all the below settings based on these strings. Use StartsWith, EndsWith, Contains etc.
        //if (!fileName.EndsWith("_vat")) return;

        ModelImporter importer  = assetImporter as ModelImporter;
        string        name      = importer.assetPath.ToLower();
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
                importer.optimizeMesh       = false;
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
                importer.importMaterials    = true;
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

    //private void OnPostprocessMaterial(Material material) { }

    /// <summary>
    /// Runs after all assets are imported and creates any character meshes
    /// </summary>
    /// <param name="importedAssets"></param>
    /// <param name="deletedAssets"></param>
    /// <param name="movedAssets"></param>
    /// <param name="movedFromAssetPaths"></param>
    static void OnPostprocessAllAssets(string[] importedAssets, string[] deletedAssets, string[] movedAssets,
        string[] movedFromAssetPaths)
    {
        List<string> baseMeshImports = new List<string>();
 
        //Pull out the assets inside the proper folders
        foreach (string importedAsset in importedAssets)
        {
            //Debug.Log("Asset A");
            //Debug.Log(importedAsset);
            //Debug.Log(_baseString);
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
                // Debug.Log(importedAsset);
                // Debug.Log(_baseString);                
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
 
                //Begin construction
                ConstructPrefab(baseMaterial);
            }
        }
    }

    /// <summary>
    /// Initial call to create a character mesh. 
    /// </summary>
    /// <param name="importedFilePath"></param>
    private static void ConstructPrefab(string importedFilePath)
    {
        //Load the asset from the project
        var importedFile = (GameObject) AssetDatabase.LoadAssetAtPath(importedFilePath, typeof(GameObject));
 
        //Instantiate the prefab in to the scene so we can start to work with it
        var instantiatedBaseMesh = GameObject.Instantiate(importedFile);
 
        //5. Create a material file to contain the textures
        CreateMaterial();

        //8.Grab all the mesh objects and apply the new material to it.
        ApplyMaterialsToMesh(instantiatedBaseMesh);
 
        //Start putting the prefab together
        CreatePrefab(instantiatedBaseMesh);
    }


    /// <summary>
    /// Sets the material on the asset.
    /// </summary>
    /// <param name="material"></param>
    public static void CreateMaterial()
    {
        string materialName = _assetName + "_mat_vat.mat";
 
        //clear out the main material in case it is filled in from previous import

        _mainMaterial = null;
 
        //Make sure the materials directoy exists before adding stuff to it
        if (!Directory.Exists(MaterialsPath))
        {
            Directory.CreateDirectory(MaterialsPath);
        }
 
        // Debug.Log(Directory.Exists(MaterialsPath));
 
        //Check all the files in the directory for the main material
        foreach(var file in Directory.GetFiles(MaterialsPath, "*.mat", SearchOption.TopDirectoryOnly))
        {                
            //compare strings an check for the materialname in the file
            Match match = Regex.Match(file, materialName, RegexOptions.IgnoreCase);
 
            //If the file exists, set the main material variable with the project file
            if (match.Success)
            {
                _oldMaterial = (Material)AssetDatabase.LoadAssetAtPath(file, typeof(Material));
                // _newMaterial.CopyPropertiesFromMaterial(_oldMaterial);
            }
        }

        //create a new material
        var tempMaterial = new Material(Shader.Find("LaidlawFX/Rigid"));
        string tempName = "temp_mat_vat.mat";
        //save material to the project directory
        AssetDatabase.CreateAsset(tempMaterial, Path.Combine(MaterialsPath, tempName));

        //load up the the new material and store it
        _mainMaterial = (Material)AssetDatabase.LoadAssetAtPath(Path.Combine(MaterialsPath, tempName), typeof(Material));
        _mainMaterial.CopyPropertiesFromMaterial(_oldMaterial);
        AssetDatabase.DeleteAsset(Path.Combine(MaterialsPath, materialName));
        AssetDatabase.RenameAsset(Path.Combine(MaterialsPath, tempName),materialName);        
        //_mainMaterial.CopyPropertiesFromMaterial(_tempMaterial);

        // }
        //Grab the position texture if it exists
        string texturePath = GetFilesPathNotMeta(TexturePath, _assetName + "_pos_vat"); 
 
        Texture2D posTex = (Texture2D)AssetDatabase.LoadAssetAtPath(texturePath, typeof(Texture2D));
 
        if (posTex != null)
        {
            _mainMaterial.SetTexture("_posTex", posTex);
        }
 
        //Grab the rotation map path if it exists
        texturePath = GetFilesPathNotMeta(TexturePath, _assetName + "_rot_vat");
 
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

    /// <summary>
    /// Applys the material to all meshes in the prefab
    /// Doesnt allow for multiple meshes or materials
    /// </summary>
    private static void ApplyMaterialsToMesh(GameObject baseMesh)
    {
        foreach (var mesh in baseMesh.GetComponentsInChildren<Renderer>())
        {
            mesh.sharedMaterial = _mainMaterial;
        }
    }
 
    /// <summary>
    /// Creates a prefab with materials 
    /// </summary>
    /// <param name="assetPrefab"></param>
    private static void CreatePrefab(GameObject assetPrefab)
    {
        Selection.activeGameObject = assetPrefab;
 
        //Set the name of the object to be the prefab name
        assetPrefab.name = _assetName;
        
        //12. Save\Create the prefab in the project hierarchy
        var folder = Directory.CreateDirectory(PrefabPath); 
        string prefabSavePath = string.Format("{0}/Prefabs/{1}_PF.prefab", _basePath, _assetName);
        PrefabUtility.SaveAsPrefabAsset(assetPrefab,prefabSavePath);
 
        GameObject.DestroyImmediate(assetPrefab);
    }

    /// <summary>
    /// Return the raw fbx file, not a meta file
    /// </summary>
    /// <param name="filePath">Root Directory to start with</param>
    /// <param name="searchString"> string to search in the file path</param>
    /// <returns></returns>
    private static string GetFilesPathNotMeta(string filePath, string searchString)
    {
        return Directory.GetFiles(filePath).FirstOrDefault(
            x => x.IndexOf(searchString, StringComparison.OrdinalIgnoreCase) >= 0 &&
                 x.IndexOf(".meta") < 0);
    }

    #endregion Post Processors

    #endregion Methods
}