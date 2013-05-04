import os
import stat
import sys
import grp
import shutil

# Get numerical GID for project
GID = grp.getgrnam(os.environ['PROJECT_NAME']).gr_gid

# read/write access for user, group and others
PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH #| stat.S_IWOTH

def clobberPermissions(path):
    '''Force proper permissions on the file pointed to by path'''
    try:
        os.chown(path, -1, GID)
    except Exception as e:
        sys.stderr.write('Error occured while changing group: ' + str(e) + '\n')
    else:
        sys.stderr.write('Group forcefully changed: ' + str(path) + '\n')
    finally:
        pass

    try:
        os.chmod(path, PERMISSIONS)
    except Exception as e:
        sys.stderr.write('Error occured while changing permissions: ' + str(e) + '\n')
    else:
        sys.stderr.write('Forcefully changed permissions: ' + str(path) + '\n')
    finally:
        pass

def copy(src, dst):
    '''Copy with proper permissions'''
    clobberPermissions(src)

    shutil.copy(src, dst)

    clobberPermissions(dst)

    #sys.stderr.write('Files copied: ' + str(src) + '; ' + str(dst) + '\n')

def move(src, dst):
    '''Copy with proper permissions'''
    clobberPermissions(src)

    shutil.move(src, dst)

    clobberPermissions(dst)

    #sys.stderr.write('Files moved: ' + str(src) + '; ' + str(dst) + '\n')

