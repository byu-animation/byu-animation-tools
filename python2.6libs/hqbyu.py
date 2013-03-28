import os
import xmlrpclib as xrl

SERVER_URI = 'http://hqueue:5000'

def hqJob(command, name='No Name Given', parent=None, priority=0, description=None):
    import hutil

    job = {'name':str(name), 'command':str(command)}
    job['submittedBy'] = hutil.username.currentUserName()    
    job['shell'] = 'bash'
    job['priority'] = priority

    if description != None:
        job['description'] = str(description)

    if parent != None:
        try:
            childList = parent['children']
        except KeyError as ke:
            childList = list()
            parent['children'] = childList

        child = job
        job = parent
        childList.append(child)
        job['children'] = childList

    return job

def submitJob(job, alternate_server=None):
    hq_server = None

    if alternate_server != None:
        hq_server = xrl.ServerProxy('http://' + alternate_server)
    else:
        hq_server = xrl.ServerProxy(SERVER_URI)

    if job == None:
        raise 'No job given!'

    jobid = hq_server.newjob(job)

    return jobid

def nukeJob(nkfile, jobname=None, jobpriority=0):
    if jobname == None or jobname.strip() == '':
        jobname = os.path.basename(nkfile)

    command = '/usr/local/Nuke6.3v9/Nuke6.3 -t --nukex --sro --cont -x -V 2 '
    command += nkfile

    #tmpcmd = 'echo "Waiting..."; sleep 30; echo "Done!"'

    nkfilejob = hqJob(command, name=jobname, priority=jobpriority)
    submitJob(nkfilejob)

# TODO: Implement maya batch job processing
def mayaJob(mayafile, jobname=None, jobpriority=0):
    pass

