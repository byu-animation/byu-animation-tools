# NAME: HoudiniEnvLightRIB.py ( Python )
#
# COMMENTS:     Wrangler for the HoudiniEnvLight object.

import os
import soho
import hou, shopclerks
from soho import SohoParm

# Properties in the HoudiniEnvLight object which get mapped to the
# light shader.
lshaderParms = {
    'r'               : SohoParm('r', 'real', [0,0,0], False),
    
    'light_type'            : SohoParm('light_type',        'string', ['point'], False),
    'light_color'           : SohoParm('light_color',      'real', [.5,.5,.5], False),
    'light_intensity'       : SohoParm('light_intensity',     'real', [1], False),
    
    'shadow_type'           : SohoParm('shadow_type','string', ['raytrace'], False),

    'light_contribdiff'     : SohoParm('light_contribdiff', 'int', [1], False),
    'light_contribspec'     : SohoParm('light_contribspec', 'int', [1], False),

    'env_mode'              : SohoParm('env_mode', 'string', ['direct'], False),
    'env_map'               : SohoParm('env_map', 'string', [''], False),
    'env_clipy'             : SohoParm('env_clipy', 'int', [0], False),
    'vm_samplingquality'    : SohoParm('vm_samplingquality', 'real', [1], False),
    'env_domaxdist'         : SohoParm('env_domaxdist', 'int', [0], False),
    'env_maxdist'           : SohoParm('env_maxdist', 'real', [10], False),
    'env_angle'             : SohoParm('env_angle', 'real', [90], False),
    'env_doadaptive'        : SohoParm('env_doadaptive', 'int', [0], False),
    'shadow_intensity'      : SohoParm('shadow_intensity', 'real', [1], False),
    'shadow_transparent'    : SohoParm('shadow_transparent', 'int', [1], False),
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
    shadow_type         = plist['shadow_type'].Value[0]
    isdiff              = plist['light_contribdiff'].Value[0]
    isspec              = plist['light_contribspec'].Value[0]

    env_mode            = plist['env_mode'].Value[0]
    env_map             = plist['env_map'].Value[0]
    env_clipy           = plist['env_clipy'].Value[0]
    samplingquality     = plist['vm_samplingquality'].Value[0]
    env_domaxdist       = plist['env_domaxdist'].Value[0]
    env_maxdist         = plist['env_maxdist'].Value[0]
    env_angle           = plist['env_angle'].Value[0]
    env_doadaptive      = plist['env_doadaptive'].Value[0]
    shadow_intensity    = plist['shadow_intensity'].Value[0]
    shadow_type         = plist['shadow_type'].Value[0]
    shadow_transparent  = plist['shadow_transparent'].Value[0]

    rotates = plist['r'].Value

    if len(light_color) == 1:
        light_color.append(light_color[0])
    if len(light_color) == 2:
        light_color.append(light_color[1])

    shader = '"h_envlight" %s [%g %g %g]' % \
            ( _uc('lightcolor'),
                light_color[0] * light_intensity,
                light_color[1] * light_intensity,
                light_color[2] * light_intensity)
    
    shader += ' %s [%g]' % (_uf('samplingquality'), samplingquality)

    shader += ' %s [%g %g %g]' % (_uv('env_rotate'),
                hou.hmath.degToRad(rotates[0]),
                hou.hmath.degToRad(rotates[1]),
                hou.hmath.degToRad(rotates[2]))

    if env_mode != 'direct':
        shader += ' %s ["%s"]' % (_us('env_mode'), env_mode)
    
    if env_mode == 'background':
        shader += ' %s ["%s"]' % (_us('env_map'), 'raytrace')
     
    if env_mode == 'occlusion':
        if env_angle != 90:
            shader+= ' %s [%g]' % (_uf('env_angle'), hou.hmath.degToRad(env_angle))
        # Max distance and adaptive samping apply if we are using occlusion
        if env_domaxdist == 1:
            shader += ' %s [%g]' % (_uf('env_domaxdist'), env_domaxdist)
            shader += ' %s [%g]' % (_uf('env_maxdist'), env_maxdist)
        if env_doadaptive != 0:
            shader += ' %s [%g]' % (_uf('env_doadaptive'), env_doadaptive)
     
    if env_map != '' and env_mode != 'background':
        shader += ' %s ["%s"]' % (_us('env_map'), env_map)
   
    if env_clipy != 0:
        shader += ' %s ["1"]' % (_uf('env_clipy'), env_clipy)
    
    if not isdiff:
        shader += ' "float __nondiffuse" [1]'
    if not isspec or env_mode == 'occlusion':
        shader += ' "float __nonspecular" [1]'

    if shadow_type != 'raytrace':
        shader += ' %s ["off"]' % (_us('shadow_type'))
    else:
        if shadow_intensity != 1:
            shader += ' %s [%g]' % (_uf('shadow_intensity'), shadow_intensity)
        if shadow_transparent != 1:
            shader += ' %s ["primitive"]' % _us('shadow_hitmode')

    value[:] = [shader]
    return True


parmMap = {
    
    'shop_lightpath'    :       light_shader,

    # All other properties can be added by the user as spare
    # properties if they want.
}

class hEnvlightRIB:
    def __init__(self, obj, now, version):
        self.Label = 'Houdini Environment Light RIB'
        self.Version = version

    def evalParm(self, obj, parm, now):
        key = parm.Houdini      # Which houdini parameter is being evaluated?
        if parmMap.has_key(key):
            return parmMap[key](obj, now, parm.Value)
        return obj.evalParm(parm, now)

def registerLight(list):
    key = 'HoudiniEnvLight-RIB'
    if not list.has_key(key):
        list[key] = hEnvlightRIB

