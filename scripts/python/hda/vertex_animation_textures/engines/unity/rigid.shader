Shader "Volumetrica/Rigid" {
    Properties {
        _Color          ("Color", Color)                        = (1,1,1,1)
        _MainTex        ("Albedo (RGB)", 2D)                    = "white" {}
        _Glossiness     ("Smoothness", Range(0,1))              = 0.5
        _Metallic       ("Metallic", Range(0,1))                = 0.0
        _numOfFrames    ("Number Of Frames", int)               = 240
        _speed          ("Speed", Float)                        = 0.33
        [MaterialToggle] _animateTime ("Animate Time", Float)   = 0
        _frameNumber    ("FrameNumber", int)                    = 0                 
        _posTex         ("Position Map (RGB)", 2D)              = "white" {}            
        _posMax         ("Position Max", Float)                 = 1.0
        _posMin         ("Position Min", Float)                 = 0.0
        _rotTex         ("Rotation Map (RGB)", 2D)              = "grey" {}
        _pivMax         ("Pivot Max", Float)                    = 1.0
        _pivMin         ("Pivot Min", Float)                    = 0.0
        [MaterialToggle] _packPscale ("Pack Pscale", Float)     = 0             
        _scaleTex       ("Scale Map (RGB)", 2D)                 = "white" {}
        _scaleMax       ("Scale Max", Float)                    = 0.0
        _scaleMin       ("Scale Min", Float)                    = 0.0
        _colTex         ("Colour Map (RGB)", 2D)                = "white" {}                    
    }
    SubShader {
        Tags { "RenderType"="Opaque" }
        LOD 200
        
        CGPROGRAM
        // Physically based Standard lighting model, and enable shadows on all light types
        #pragma surface surf Standard addshadow vertex:vert

        // Use shader model 3.0 target, to get nicer looking lighting
        #pragma target 3.0
        #pragma fragmentoption ARB_precision_hint_nicest
        sampler2D     _MainTex;
        sampler2D     _posTex;
        sampler2D     _rotTex;
        sampler2D     _scaleTex;
        sampler2D     _colTex;  
        uniform float _packPscale;                                             
        uniform float _animateTime;
        uniform float _posMax;
        uniform float _posMin;                          
        uniform float _pivMax;
        uniform float _pivMin;
        uniform float _scaleMax;
        uniform float _scaleMin;
        uniform float _speed;   
        uniform int   _numOfFrames;
        uniform int   _frameNumber;        

        struct Input {
            float2 uv_MainTex;
            float4 vcolor : COLOR;
        };

        half   _Glossiness;
        half   _Metallic;
        fixed4 _Color;

        // Add instancing support for this shader. You need to check 'Enable Instancing' on materials that use the shader.
        // See https://docs.unity3d.com/Manual/GPUInstancing.html for more information about instancing.
        // #pragma instancing_options assumeuniformscaling
        UNITY_INSTANCING_BUFFER_START(Props)
                // put more per-instance properties here
        UNITY_INSTANCING_BUFFER_END(Props)

        //vertex function
        void vert(inout appdata_full v){
            //calculate time
            float rate           = frac(_Time.y * _speed);                
            if (_animateTime){
                rate             = ((1.0 * _frameNumber) / (1.0 * _numOfFrames));
            }

            //calculate uv coordinates
            float timeInFrames   = ((ceil(rate * _numOfFrames))/_numOfFrames);

            //get position and rotation(quaternion) from textures
            float4 texLookup     = float4(v.texcoord1.x, (1 - timeInFrames) + v.texcoord1.y, 0, 0);
            float4 texPos        = tex2Dlod(_posTex,    texLookup);
            float4 texRot        = tex2Dlod(_rotTex,    texLookup);         
            float3 texScale      = tex2Dlod(_scaleTex,  texLookup);  
            float3 texCol        = tex2Dlod(_colTex,    texLookup);                       
            //expand normalised position texture values to world space
            float expandPos      = _posMax - _posMin;
            texPos.xyz          *= expandPos;
            texPos.xyz          += _posMin;
            //texPos.x            *= -1; //from unreal space
            //texPos.xyz           = texPos.xzy; //from unreal space 

            //calculate scale
            float3 scale        = texScale.xyz;
            if (_packPscale){
                scale           = texPos.w;
            } 
            //expand normalised position texture values to world space
            float expandScale    = _scaleMax - _scaleMin;
            scale               *= expandScale;
            scale               += _scaleMin;

            //expand normalised pivot vertex colour values to world space
            float expandPiv      = _pivMax - _pivMin;
            float3 pivot         = v.color.rgb;
            pivot.xyz           *= expandPiv;
            pivot.xyz           += _pivMin;
            //pivot.x             *= -1; //from unreal space   
            //pivot                = pivot.xzy; //from unreal space                  
            float3 atOrigin      = (v.vertex.xyz - pivot) *(scale+1);

            //calculate rotation
            texRot              *= 2.0;
            texRot              -= 1.0;          
            //texRot.x             = -texRot.x; //from unreal space
            //texRot.xyzw          = texRot.xzyw; //from unreal space
                        
            float3 rot           = atOrigin + 2.0 * cross(texRot.xyz, cross(texRot.xyz, atOrigin) + texRot.w * atOrigin);                     

            v.vertex.xyz         = rot;
            v.vertex.xyz        += pivot;
            v.vertex.xyz        += texPos.xyz;

            //calculate normal
            float3 rotNormal     = v.normal + 2.0 * cross(texRot.xyz, cross(texRot.xyz, v.normal) + texRot.w * v.normal);
            v.normal             = rotNormal;

            //set vertex colour
            v.color.rgb          = texCol;            
        }

        void surf (Input IN, inout SurfaceOutputStandard o) {
            // Albedo comes from a texture tinted by color
            fixed4 c             = tex2D (_MainTex, IN.uv_MainTex) * _Color ;
            o.Albedo             = c.rgb * IN.vcolor.rgb;         
            // Metallic and smoothness come from slider variables
            o.Metallic           = _Metallic;
            o.Smoothness         = _Glossiness;
            o.Alpha              = c.a;
        }
        ENDCG
    }
    FallBack "Diffuse"
}
