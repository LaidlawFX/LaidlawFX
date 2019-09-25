/* 
    An editor script that customizes the way assets are imported based on their file names
    Sarper Soher                                                 
    http://sarpersoher.com/unity3d/conditional-asset-importer/
*/

using UnityEditor;
using UnityEngine;

internal sealed class VAT_AssetImporter : AssetPostprocessor {
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

    private void OnPreprocessAudio() { }
    
    #endregion Pre Processors

    #region Post Processors 

    // Post processors get invoked after the asset is sucessfully imported, now we can edit the crated assets from our source files

    private void OnPostprocessTexture(Texture2D import) { }

    private void OnPostprocessModel(GameObject import) { }

    private void OnPostprocessAudio(AudioClip import) { }

    #endregion Post Processors

    #endregion Methods
}