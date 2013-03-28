# NAME: HoudiniIndirectLightRIB.py ( Python )
#
# COMMENTS:     Wrangler for the HoudiniIndirectLight object.

import os
import soho
import hou
from soho import SohoParm

# Properties in the HoudiniIndirectLight object which get mapped to the
# light shader.
lshaderParms = {
    'r'               : SohoParm('r', 'real', [0,0,0], False),
    
    'light_type'            : SohoParm('light_type',        'string', ['point'], False),
    'light_color'           : SohoParm('light_color',      'real', [.5,.5,.5], False),
    'light_intensity'       : SohoParm('light_intensity',     'real', [1], False),
    
    'light_contribdiff'     : SohoParm('light_contribdiff', 'int', [1], False),
    'light_contribspec'     : SohoParm('light_contribspec', 'int', [1], False),

    'vm_samplingquality'    : SohoParm('vm_samplingquality', 'real', [1], False),
    'render_domaxdist'         : SohoParm('render_domaxdist', 'int', [0], False),
    'render_maxdist'           : SohoParm('render_maxdist', 'real', [10], False),
    'render_angle'             : SohoParm('render_angle', 'real', [90], False),
    'render_doadaptive'        : SohoParm('render_doadaptive', 'int', [0], False),
}

def _fixpath(path):
    if path.startswith('temp:'):
        # Strip off the leading 'temp:'
        path = path.replace('temp:', '')
        # Insert the houdini temp directory
        path = os.path.join(hou.getenv('HOUDINI_TEMP_DIR'), path)
    # "fix" any embedded quotes in the path
    return path.replace('"', '\\"')

def _uf(name, alen=-1):
    if alen >= 0:
        return '"uniform float[%d] %s"' % (alen, name)
    return '"uniform float %s"' % name

def _uc(name, alen=-1):
    if alen >= 0:
        return '"uniform color[%d] %s"' % (alen, name)
    return '"uniform color %s"' % name

def _uv(name, alen=-1):
    if alen >= 0:
        return '"uniform vector[%d] %s"' % (alen, name)
    return '"uniform vector %s"' % name

def _us(name):
    return '"uniform string %s"' % name

def light_shader(obj, now, value):
    if obj.evalShader('shop_lightpath', now, value):
        if value[0]:
            return True

    plist = obj.evaluate(lshaderParms, now)
    ltype = plist['light_type'].Value[0]

    light_color         = plist['light_color'].Value
    light_intensity     = plist['light_intensity'].Value[0]

    samplingquality     = plist['vm_samplingquality'].Value[0]
    render_domaxdist       = plist['render_domaxdist'].Value[0]
    render_maxdist         = plist['render_maxdist'].Value[0]
    render_angle           = plist['render_angle'].Value[0]
    render_doadaptive      = plist['render_doadaptive'].Value[0]

    rotates = plist['r'].Value

    if len(light_color) == 1:
        light_color.append(light_color[0])
    if len(light_color) == 2:
        light_color.append(light_color[1])

    shader = '"h_gilight" %s [%g %g %g]' % \
            ( _uc('lightcolor'),
                light_color[0] * light_intensity,
                light_color[1] * light_intensity,
                light_color[2] * light_intensity)
    
    shader += ' %s [%g]' % (_uf('samplingquality'), samplingquality)

    if render_angle != 90:
        shader+= ' %s [%g]' % (_uf('render_angle'), hou.hmath.degToRad(render_angle))
    
    if render_domaxdist == 1:
        shader += ' %s [%g]' % (_uf('render_maxdist'), render_maxdist)
    
    if render_doadaptive != 0:
            shader += ' %s [%g]' % (_uf('render_doadaptive'), render_doadaptive)

    if ltype == 'indirectglobal' or ltype == 'indirect':
        value[:] = [shader]
    else:
        value[:] = ['null']
    return True


parmMap = {
    
    'shop_lightpath'    :       light_shader,

    # All other properties can be added by the user as spare
    # properties if they want.
}

class hGIlightRIB:
    def __init__(self, obj, now, version):
        self.Label = 'Houdini Indirect Light RIB'
        self.Version = version

    def evalParm(self, obj, parm, now):
        key = parm.Houdini      # Which houdini parameter is being evaluated?
        if parmMap.has_key(key):
            return parmMap[key](obj, now, parm.Value)
        return obj.evalParm(parm, now)

def registerLight(list):
    key = 'HoudiniIndirectLight-RIB'
    if not list.has_key(key):
        list[key] = hGIlightRIB

