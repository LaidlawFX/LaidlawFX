Shader "LaidlawFX/Sprite" {
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
        _height         ("Height", Float)                       = 1.0
        _width          ("Width", Float)                        = 1.0           
        
        [MaterialToggle] _packPscale ("Pack Pscale", Float)     = 0
        _scaleTex       ("Scale Map (RGB)", 2D)                 = "white" {}
        _scaleMax       ("Scale Max", Float)                    = 1.0
        _scaleMin       ("Scale Min", Float)                    = 0.0
        _colTex         ("Colour Map (RGB)", 2D)                = "white" {}
    }
    SubShader {
        Tags { "Queue"="Transparent" "RenderType"="Opaque" }
        LOD 200
        Blend SrcAlpha OneMinusSrcAlpha 
        CGPROGRAM
        // Physically based Standard lighting model, and enable shadows on all light types
        #pragma surface surf Standard alpha:fade vertex:vert

        // Use shader model 3.0 target, to get nicer looking lighting
        #pragma target 3.0

        sampler2D     _MainTex;
        sampler2D     _posTex;
        
        sampler2D     _scaleTex;
        sampler2D     _colTex;              
        uniform float _packPscale;
        uniform float _animateTime;
        uniform float _posMax;
        uniform float _posMin;
        uniform float _scaleMax;
        uniform float _scaleMin;            
        uniform float _speed;
        uniform float _height;
        uniform float _width;
        uniform int   _numOfFrames;
        uniform int   _frameNumber;

        struct Input {
            float2 uv_MainTex;
            float4 vcolor : COLOR ; //Vertex Color
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
            float timeInFrames   = ((ceil(rate * _numOfFrames))/_numOfFrames) + (1.0/_numOfFrames);

            //get position and colour from textures
            float4 texLookup     = float4(v.texcoord1.x, (1 - timeInFrames) + v.texcoord1.y, 0, 0);
            float4 texPos        = tex2Dlod(_posTex,texLookup);
            float3 texScale      = tex2Dlod(_scaleTex,texLookup); 
            float3 texCol        = tex2Dlod(_colTex,texLookup);

            //expand normalised position texture values to world space
            float expandPos      = _posMax - _posMin;
            texPos.xyz          *= expandPos;
            texPos.xyz          += _posMin;

            //calculate scale
            float3 scale        = texScale.xyz;
            if (_packPscale){
                scale           = texPos.w;
            } 
            //expand normalised position texture values to world space
            float expandScale    = _scaleMax - _scaleMin;
            scale               *= expandScale;
            scale               += _scaleMin;

            //create camera facing billboard based on uv coordinates
            float3 cameraF       = float3(v.texcoord.x - 0.5, v.texcoord.y - 0.5, 0);
            cameraF             *= float3(_width, _height, 1);
            cameraF             *= scale;
            cameraF              = mul(cameraF, UNITY_MATRIX_MV);          
            v.vertex.xyz         = cameraF;
            v.vertex.xyz        += texPos.xyz;
            
            //set vertex colour
            v.color.rgb          = texCol;
        }

        void surf (Input IN, inout SurfaceOutputStandard o) {
            // Albedo comes from a texture tinted by color
            fixed4 c             = tex2D (_MainTex, IN.uv_MainTex) * _Color;
            o.Albedo             = c.rgb * IN.vcolor.rgb; //multiply existing albedo map by vertex colour 
            // Metallic and smoothness come from slider variables
            o.Metallic           = _Metallic;
            o.Smoothness         = _Glossiness;
            o.Alpha              = c.a;
        }
        ENDCG
    }
    FallBack "Diffuse"
}
