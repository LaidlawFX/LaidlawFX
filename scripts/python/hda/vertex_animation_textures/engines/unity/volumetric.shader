Shader "Volumetrica/Volumetric" {
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
        


        [MaterialToggle] _packNorm ("Pack Normal", Float)       = 1
        _normTex        ("Normal Map (RGB)", 2D)                = "grey" {}


        _colTex         ("Colour Map (RGB)", 2D)                = "white" {}

        _uvTex          ("UV Map (RGB)", 2D)                    = "white" {} 

        [MaterialToggle] _temp_LookAt ("Temp LookAt", Float)    = 0  
        _LookAt         ("LookAt", Range(0,1))                  = 0.0
        _widthTex       ("Texture Width", Float)                = 1024
        _heightTex      ("Texture Height", Float)               = 1024                 
        [MaterialToggle] _temp_Script ("Test Script", Float)    = 0

        _testColor      ("Test Color", Color)                   = (0,0,1,1)                           
    }
    SubShader {
        Tags { "RenderType"="Opaque" }
        LOD 200
        Cull Off
        CGPROGRAM
        // Physically based Standard lighting model, and enable shadows on all light types
        #pragma surface surf Standard addshadow vertex:vert

        // Use shader model 3.0 target, to get nicer looking lighting
        #pragma target 3.0

        sampler2D        _MainTex;
        sampler2D        _posTex;
        sampler2D        _uvTex;
        sampler2D        _normTex;
        sampler2D        _colTex;
        uniform float    _packNorm;
        uniform float    _animateTime;
        uniform float    _posMax;
        uniform float    _posMin;  
        uniform float    _speed;
        uniform int      _numOfFrames;
        uniform int      _frameNumber;
        uniform float4x4 _LookAt_Matrix;
        uniform float3   _neck_pos;
        uniform float3   _nose_dir;
        uniform float3   _tilt_dir;
        uniform float    _temp_LookAt; 
        uniform float    _LookAt; 
        uniform float    _widthTex;
        uniform float    _heightTex;                                
        uniform float    _temp_script;        
        uniform float4   _testColor;


        struct Input {
            float2 uv_MainTex;
            float4 vcolor : COLOR; //Vertex Color
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
            
            //get position, normal, and uv from textures
            float4 texLookup     = float4(v.texcoord1.x, (1 - timeInFrames) + v.texcoord1.y, 0, 0);
            float4 texPos        = tex2Dlod(_posTex,  texLookup);
            float4 texUV         = tex2Dlod(_uvTex,   texLookup);             
            float3 texNorm       = tex2Dlod(_normTex, texLookup);            
            float3 texCol        = tex2Dlod(_colTex,  texLookup);

            // Define shared Index
            //float Index          = texUV.w

            //expand normalised position texture values to world space
            float expandPos      = _posMax - _posMin;
            texPos.xyz          *= expandPos;
            texPos.xyz          += _posMin;
            float3 pos           = texPos.xyz;

            float3 norm          = v.normal.xyz;
            //calculate normal
            if (_packNorm){
                //decode float to float2
                float alpha      = texPos.w * 1024;
                float2 f2;
                f2.x             = floor(alpha / 32.0) / 31.5;
                f2.y             = (alpha - (floor(alpha / 32.0)*32.0)) / 31.5;

                //decode float2 to float3
                float3 f3;
                f2              *= 4;
                f2              -= 2;
                float f2dot      = dot(f2,f2);
                f3.xy            = sqrt(1 - (f2dot/4.0)) * f2;
                f3.z             = 1 - (f2dot/2.0);
                f3               = clamp(f3, -1.0, 1.0);
                norm             = f3;
            } else {
                texNorm         *= 2;
                texNorm         -= 1; 
                norm             = texNorm;
            }
            //calculate normal
            if (_temp_LookAt){
                // Sample 3 pixels of UVs
                float     texWidth      = _widthTex;
                float     texHeight     = _heightTex;
                // sample the texture but only at positions corresponding to whole pixels
                // multiplying the position by the texture width and then flooring it should
                // bring it into the [0, 1023] interval with only integer values
                // dividing it by the texture width again should return the interval to [0, 1]
                float2    neck_uv       = float2(floor(v.uv.x * texWidth) / texWidth, floor(v.uv.y * texHeight) / texHeight);
                fixed4    neck_pos      = tex2D(_MainTex, neck_uv);
                float2    nose_uv       = float2(floor(v.uv.x * texWidth) / texWidth+1.0, floor(v.uv.y * texHeight) / texHeight);
                fixed4    nose_dir      = tex2D(_MainTex, nose_uv);
                float2    tilt_uv       = float2(floor(v.uv.x * texWidth) / texWidth+2.0, floor(v.uv.y * texHeight) / texHeight);
                fixed4    tilt_dir      = tex2D(_MainTex, tilt_uv);



                // Define LookAt Matte
                float    LookAt_Matte   = texUV.z *_LookAt;  

                //create camera facing billboard based on uv coordinates;
                float4x4 LookAt_Matrix  = _LookAt_Matrix;

                //Offset head position so rotation is at the origin
                pos.y                  -= _pos_head.y; 

                // Rotate LookAt
                float3   vPos           = mul(pos,LookAt_Matrix);
                float3   vNorm          = normalize(mul(norm,LookAt_Matrix));

                //Blend original mesh with deformed mesh
                vPos                    = lerp(pos,  vPos, LookAt_Matte  );
                vPos.y                 += _pos_head.y; //Move head back to world location      
                vNorm                   = normalize(lerp(norm, vNorm, LookAt_Matte));

                //Set deformed mesh
                v.vertex.xyz            = vPos; 
                v.normal.xyz            = vNorm; 
            } else {
                v.vertex.xyz            = pos; 
                v.normal.xyz            = norm;
            }   

            // Set the volumetric texture
            v.texcoord.xy        = texUV.xy                       

            //set vertex colour in case of test.
            if (_temp_script){
                v.color.rgba     = lerp(_Color,  _testColor, MatteTex.r  );
            } else {
                v.color.rgb      = texCol;
            }

        }

        void surf (Input IN, inout SurfaceOutputStandard o) {
            // Albedo comes from a texture tinted by color
            fixed4 c             = tex2D (_MainTex, IN.uv_MainTex) * _Color;
            o.Albedo             = c.rgb * IN.vcolor.rgb;  //multiply existing albedo map by vertex colour
            // Metallic and smoothness come from slider variables
            o.Metallic           = _Metallic;
            o.Smoothness         = _Glossiness;
            o.Alpha              = c.a;
        }
        ENDCG
    }
    FallBack "Diffuse"
}
