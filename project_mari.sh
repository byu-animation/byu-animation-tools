# Coded by Andrew Rasmussen 2013. When it is terrible or breaks blame him. Or bake him pity cookies.
# Start Up Script for Mari in the pipeline, setting all the variables.
# ------------------------------------------------------------------------------


MARI_SCRIPT_PATH = "/groups/owned/byu-animation-tools/mari-tools/"

# source project environment
DIR=`dirname $0`
source ${DIR}/project_env.sh

export CURRENT_PROG='Mari'

# Change directories so current directory is not in the tools folder
cd ${USER_DIR}

echo "Starting Mari..."
/usr/local/Mari2.0v1/mari












cd /path/to/mari
# Normal terminal mode
./mari -t
# Terminal mode - run the script, then show a Python input prompt
./mari -t /path/to/script_name.py


CERTIFICATES = 'CERTIFICATES' #: Security certificates. 
COLOR = 'COLOR' #: L{Color} data. 
C_API_DOCS = 'C_API_DOCS' #: C API documentation. 
DEFAULT_ARCHIVE = 'MARI_DEFAULT_ARCHIVE_PATH' #: The default path to load and save project archives. 
DEFAULT_CAMERA = 'MARI_DEFAULT_CAMERA_PATH' #: The default path to load and save cameras and projectors. 
DEFAULT_EXPORT = 'MARI_DEFAULT_EXPORT_PATH' #: The default path to export textures to. 
DEFAULT_GEO = 'MARI_DEFAULT_GEOMETRY_PATH' #: The default path to load geometry from. 
DEFAULT_IMAGE = 'MARI_DEFAULT_IMAGE_PATH' #: The default path to load and save reference images. 
DEFAULT_IMPORT = 'MARI_DEFAULT_IMPORT_PATH' #: The default path to import textures from. 
DEFAULT_RENDER = 'MARI_DEFAULT_RENDER_PATH' #: The default path to save renders such as turntables. 
DEFAULT_SHELF = 'MARI_DEFAULT_SHELF_PATH' #: The default path to load and save shelf files. 
EXAMPLES = 'EXAMPLES' #: Example data assets. 
GRADIENTS = 'GRADIENTS' #: Brush gradients. 
HELP = 'HELP' #: Help documentation resources. 
ICONS = 'ICONS' #: Tool bar and menu item icons. 
IMAGES = 'IMAGES' #: General system images. 
LOGOS = 'LOGOS' #: Logo images for the application. 
LUTS = 'LUTS' #: LUT data. 
MEDIA = 'MEDIA' #: Top level media directory. 
MISC = 'MISC' #: Other miscellaneous data. 
QT_PLUGINS = 'QT_PLUGINS' #: Qt plug-ins. 
SCRIPT_DOCS = 'SCRIPT_DOCS' #: Python documentation. 
SETTINGS = 'SETTINGS' #: Default settings. 
SHADERS = 'SHADERS' #: Built-in shader code. 
SYSTEM_SCRIPTS = 'SCRIPTS' #: Built-in Python scripts - AppDir/Media/Scripts. 
USER = 'MARI_USER_PATH' #: Root of the default user path - default: ~/Mari. 
USER_PLUGINS = 'MARI_PLUGINS_PATH' #: A list of paths to load custom user plug-ins from - default: ~/Mari/Plugins. 
USER_SCRIPTS = 'MARI_SCRIPT_PATH' #: A list of paths to run scripts from - default: ~/Mari/Scripts. 
