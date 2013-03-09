import hqbyu

import hou
import hutil.username

def render():
    """Evaluate and package the HDA parameters and submit a job to HQueue.""" 
    # Build a dictionary of base parameters and add the HQueue Render-specific
    # ones.

    file = hou.ch('file')

    if file.strip() == '':
        return

    jobname = hou.ch('hq_job_name')

    priority = hou.ch('hq_priority')

    hqbyu.nukeJob(file, jobname, priority)

# Note that __name__ is not "__main__" when invoked from soho.
# __name__ is not "HQrender" when it is invoked from soho but it is when
# imported as a module
if __name__ != "HQnuke":
    render()

