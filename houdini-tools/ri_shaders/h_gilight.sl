/*
 * NAME:	h_gilight.sl ( RenderMan SL )
 *
 * COMMENTS:
 */

#define HOU_INFINITY 1e+30

light h_gilight
        (
                uniform color lightcolor = 1.0;
                uniform float samplingquality = 1;
                uniform float render_maxdist = HOU_INFINITY;
                uniform float render_angle = 1.5707963267948966; //Angle measured in radians.
                uniform float render_doadaptive = 0;

                output varying color _diffuselight = 0.0;

                output uniform float __nondiffuse = 0;
                output uniform float __nonspecular = 1;
                output uniform string __category = "indirectlight";
        )
{


    normal nN = normalize(N);

    illuminate(Ps + nN)
    {
        Cl = 0;

        color irrad = 0;

        if(samplingquality > 0)
        {
            irrad = indirectdiffuse(Ps, nN, samplingquality,
                                    "coneangle", render_angle,
                                    "maxdist", render_maxdist,
                                    "adaptive", render_doadaptive,
                                    "maxvariation", 0.0,
                                    "samplebase", 1.0,
                                    "hitmode", "shader");
        }

        _diffuselight = irrad * lightcolor;

        // Modify Ci if the surface isn't GI aware
        float aware = 0;
        surface("_gi_aware", aware);
        if( aware < 1 )
            {Cl = _diffuselight;}
    }
}
