/*
 * NAME:	h_envlight.sl ( RenderMan SL )
 *
 * COMMENTS:
 */

#define HOU_INFINITY 1e+30

float
fit(float val, omin, omax, nmin, nmax)
{
    float	t;
    t = clamp((val - omin)/(omax - omin), 0, 1);
    return mix(nmin, nmax, t);
}
    
color
fit(color v, s0, s1, d0, d1)
{
    return color(fit(comp(v,0), comp(s0,0), comp(s1,0), comp(d0,0), comp(d1,0)),
        fit(comp(v,1), comp(s0,1), comp(s1,1), comp(d0,1), comp(d1,1)),
        fit(comp(v,2), comp(s0,2), comp(s1,2), comp(d0,2), comp(d1,2)));
}

light h_envlight
        (
                uniform vector env_rotate = 0.0; // Euler rotations converted to radians
                uniform color lightcolor = 1.0;
                uniform string env_map = "";
                uniform float env_clipy = 0; //This isn't being used for anything yet.
                
                /*"background" not the same as mantra; it will attempt to 
                raytrace the scene. This may be good for legacy RSL surface 
                shaders that lack raytracing. "occlusion" will turn off 
                specular, just like Mantra does for the env light.*/
                uniform string env_mode = "direct";
                uniform float samplingquality = 1;
                uniform float env_maxdist = HOU_INFINITY;
                uniform float env_angle = PI/2; //Measured in radians.
                uniform float env_doadaptive = 0;
                uniform string shadow_type = "raytrace";
                uniform float shadow_intensity = 1.0;
                uniform string shadow_hitmode = "shader";

                output varying color _diffuselight = 0.0;
                output varying color _specularlight = 0.0;

                output varying float __nondiffuse = 0;
                output varying float __nonspecular = 0;
                output uniform string __category = "indirectlight";
        )
{
    vector ldir = L;
    normal nN = normalize(N);
    vector nI = normalize(I);

    uniform matrix objspace = matrix "object"(1);
    objspace = rotate(objspace, xcomp(env_rotate), vector(1,0,0));
    objspace = rotate(objspace, ycomp(env_rotate), vector(0,1,0));
    objspace = rotate(objspace, zcomp(env_rotate), vector(0,0,1));
    
    vector camrefl = reflect(nI, nN);
    vector objvec = vtransform(objspace, camrefl);
       
    normal objnml = ntransform(objspace, nN);
    vector Rvec = objnml;

    illuminate(Ps + nN)
    {
 
    /***********************************************************/
    /* If we are doing occlusion, ignore all other code paths. */
    /***********************************************************/

    if(env_mode == "occlusion")
    {
        color tmpenvclr = 0, tmpshadowclr = 1;

        tmpshadowclr = 1 - occlusion(Ps, nN, samplingquality,
                                "environmentmap", env_map,
                                "environmentspace", objspace,
                                "environmentcolor", tmpenvclr,
                                "coneangle", env_angle,
                                "maxdist", env_maxdist,
                                "adaptive", env_doadaptive,
                                "maxvariation", 0.0,
                                "samplebase", 1.0);

        _diffuselight = (env_map == "") ? lightcolor * tmpshadowclr: lightcolor * tmpenvclr ;
    }
    else
    {
 
        /*******************************************************/
        /* If specular is enabled. */
        /*******************************************************/
            
        if( __nonspecular < 1 )
        {
            color irradspec = 0;
            color specshadow = 1;
    
            if(env_map != "") /* Compute environment map. */
            {
                irradspec = color environment(env_map, objvec);
                _specularlight = lightcolor  * irradspec;
            }
            else // When there is no environment map then we return a flat color
            {
                _specularlight = lightcolor ;
            }

            if(shadow_type == "raytrace" && shadow_intensity > 0)
            {
                    specshadow = transmission(Ps, Ps + camrefl * HOU_INFINITY, 
                        "samples", ceil(samplingquality), "samplecone", PI/32, "hitmode", shadow_hitmode);

                    specshadow = fit(specshadow, color(0), color(1), 
                        color(1 - min(shadow_intensity, 1)), color(1));
            }
    
            _specularlight *= specshadow;
        }
    
        
        /*******************************************************/
        /* If diffuse is enabled. */
        /*******************************************************/
        
        if(__nondiffuse < 1)
        {
            color irraddiff = 0;
            color diffshadow = 1;
            
            if(env_map != "") /* Compute environment map. */
            {   
                float blur = (env_mode == "occlusion") ? env_angle : PI/2 ;
                vector rayvec = Rvec;

                gather("samplepattern", Ps, Rvec, blur, samplingquality,"ray:direction", rayvec)
                {}
                else
                {
                        irraddiff += color environment(env_map, rayvec);
                }
                
                irraddiff /= samplingquality;

                _diffuselight = lightcolor  * irraddiff;
            }
            else // When there is no environment map then we return a flat color
            {
                _diffuselight = lightcolor ;
            }
 
            if(shadow_type == "raytrace" && shadow_intensity > 0)
            {
                    diffshadow = transmission(Ps, Ps + nN * HOU_INFINITY, 
                        "samples", samplingquality,"samplecone", PI/2,
                        "hitmode", shadow_hitmode);

                    diffshadow = fit(diffshadow, color(0), color(1), 
                        color(1 - min(shadow_intensity, 1)), color(1));
            }
            
            _diffuselight *= diffshadow;
        }
    }
        // Set light color to black
        Cl = 0;
        
        // Modify Ci if the surface isn't GI aware
        float aware = 0;
        surface("_gi_aware", aware);
        if( aware < 1 )
            {Cl = _diffuselight + _specularlight;}
    }
}
