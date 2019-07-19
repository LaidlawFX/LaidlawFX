Shader "Volumetrica/Fluid" {
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

        sampler2D     _MainTex;
        sampler2D     _posTex;

        sampler2D     _normTex;
        sampler2D     _colTex;
        uniform float _packNorm;
        uniform float _animateTime;
        uniform float _posMax;
        uniform float _posMin;  
        uniform float _speed;
        uniform int   _numOfFrames;
        uniform int   _frameNumber;





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
            
            //get position and normal from textures
            float4 texLookup     = float4(v.texcoord1.x, (1 - timeInFrames) + v.texcoord1.y, 0, 0);
            float4 texPos        = tex2Dlod(_posTex,  texLookup);
            float3 texNorm       = tex2Dlod(_normTex, texLookup);            
            float3 texCol        = tex2Dlod(_colTex,  texLookup);
            //expand normalised position texture values to world space
            float expandPos      = _posMax - _posMin;
            texPos.xyz          *= expandPos;
            texPos.xyz          += _posMin;
            v.vertex.xyz         = texPos.xyz;

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
                v.normal         = f3;
            } else {
                texNorm         *= 2;
                texNorm         -= 1; 
                v.normal         = texNorm;
            }

            //set vertex colour
            v.color.rgb          = texCol;
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
