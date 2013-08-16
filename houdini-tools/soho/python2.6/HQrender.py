import os
import sys
import re
from datetime import datetime
import json

import hou
import cloud
import hutil.json
import hutil.username

import hqrop
import rendertracker

HIP_ENV_VAR_PATTERN = re.compile(r"""\$HIP(\W?)""")
JOB_ENV_VAR_PATTERN = re.compile(r"""\$JOB(\W?)""")

def render():
    """Evaluate and package the HDA parameters and submit a job to HQueue.""" 
    # Build a dictionary of base parameters and add the HQueue Render-specific
    # ones.
    parms = hqrop.getBaseParameters()
    
    use_cloud = (hou.ch("hq_use_cloud1")
        if hou.parm("hq_use_cloud1") is not None else 0)
    num_cloud_machines = (hou.ch("hq_num_cloud_machines")
        if hou.parm("hq_num_cloud_machines") is not None else 0)
    machine_type = (hou.ch("hq_cloud_machine_type")
        if hou.parm("hq_cloud_machine_type") is not None else "")
    use_output_driver = bool(use_cloud) or parms["hip_action"] != "use_ifd"

    # validate the machine type
    if machine_type not in ['c1.medium', 'c1.xlarge',
                            'm1.small', 'm1.large', 'm1.xlarge']:
        machine_type = 'c1.xlarge'

    
    parms.update({
        "assign_ifdgen_to" : hou.parm("hq_assign_ifdgen_to").evalAsString(),
        "ifdgen_clients": hou.ch("hq_ifdgen_clients").strip(),
        "ifdgen_client_groups" : hou.ch("hq_ifdgen_client_groups").strip(),
        "batch_all_frames": hou.ch("hq_batch_all_frames"),
        "frames_per_job": hou.ch("hq_framesperjob"),
        "render_frame_order": hou.parm("hq_render_frame_order").evalAsString(),
        "make_ifds": hou.ch("hq_makeifds"),
        "max_hosts_per_job": hou.ch("hq_max_hosts"),
        "min_hosts_per_job": hou.ch("hq_min_hosts"),
        "is_CPU_number_set": bool(hou.ch("hq_is_CPU_number_set")),
        "CPUs_to_use": hou.ch("hq_CPUs_to_use"),
        "output_ifd": hou.parm("hq_outputifd").unexpandedString().strip(),
        "use_output_driver" : use_output_driver,
        "use_cloud": use_cloud,
        "num_cloud_machines": num_cloud_machines,
        "cloud_machine_type" : machine_type,
        "use_render_tracker" : hou.ch("hq_use_render_tracker"),
        "delete_ifds": hou.ch("hq_delete_ifds"),
        "render_single_tile": bool(hou.ch("hq_render_single_tile")),
    })

    if use_output_driver:
        # Convert output_driver path to an absolute path.
        parms["output_driver"] = hou.ch("hq_driver").strip()
        rop_node = hou.pwd().node(parms["output_driver"])
        if rop_node:
            parms["output_driver"] = rop_node.path()

        parms["ifd_path"] = hou.parm("hq_outputifd").unexpandedString().strip()
        output_driver = hqrop.getOutputDriver(hou.pwd())

        # Turn "off" Mantra-specific parameters if there is an output driver
        # and it is not a Mantra ROP.
        if output_driver and output_driver.type().name() != "ifd":
            parms["make_ifds"] = False
            parms["min_hosts_per_job"] = 1
            parms["max_hosts_per_job"] = 1
    else:
        parms.update({
            "ifd_path" : hou.parm("hq_input_ifd").unexpandedString().strip(),
            "start_frame" : hou.ch("hq_frame_range_1"),
            "end_frame" : hou.ch("hq_frame_range_2"),
            "frame_skip" : hou.ch("hq_frame_range_3"),
            # If we are not using an output driver we are using IFDs and so
            # we won't be making them
            "make_ifds" : False,
        })

        if parms["frame_skip"] <= 0:
            parms["frame_skip"] = 1
 
    # We stop if we cannot establish a connection with the server
    if (not parms["use_cloud"]
        and not hqrop.doesHQServerExists(parms["hq_server"])):
        return None

    if "ifd_path" in parms and not parms["use_cloud"]:
        expand_frame_variables = False
        parms["ifd_path"] = hqrop.substituteWithHQROOT(
            parms["hq_server"], parms["ifd_path"], expand_frame_variables)

    # Validate parameter values.
    if (not hqrop.checkBaseParameters(parms) or
            not _checkRenderParameters(parms)):
        return
    if use_output_driver and parms["hip_action"] == "use_current_hip":
        if not hqrop.checkOutputDriver(parms["output_driver"]):
            return
        if hqrop.checkForRecursiveChain(hou.pwd()):
            hqrop.displayError(("Cannot submit HQueue job because"
                                " %s is in the input chain of %s.") 
                                % (hou.pwd().path(), parms["output_driver"]))
            return

    # If we're not supposed to run this job on the cloud, submit the job.
    # Otherwise, we'll display the file dependency dialog.
    if parms["use_cloud"]:
        # We don't want to keep the interrupt dialog open, so we exit this soho
        # script so the dialog closes and schedule an event to run the code to
        # display the dialog.
        import soho
        rop_node = hou.node(soho.getOutputDriver().getName())
        cloud.selectProjectParmsForCloudRender(
            rop_node, parms["num_cloud_machines"], parms["cloud_machine_type"])
        return

    # Automatically save changes to the .hip file,
    # or at least warn the user about unsaved changes.
    should_continue = hqrop.warnOrAutoSaveHipFile(parms)
    if not should_continue:
        return

    hqrop.submitJob(parms, _byu_troubleshoot_hq)
    #hqrop.submitJob(parms, _submitRenderJob)


def _checkRenderParameters(parms):
    """Check the values of the render-specific parameters.

    Return True if the values are valid and False otherwise.
    """

    if parms["max_hosts_per_job"] < parms["min_hosts_per_job"]:
        hqrop.displayError(
            "Max. Hosts Per Job must be greater than or equal to "
            "Min. Hosts Per Job.")
        return False
    
    # Check IFD file path.
    if parms["make_ifds"] or not parms["use_output_driver"]:
        if not parms["ifd_path"]:
            if parms["make_ifds"]:
                ifd_path_parm = hou.parm("hq_outputifd")
            elif not parms["use_output_driver"]:
                ifd_path_parm = hou.parm("hq_input_ifd")
            
            ifd_parm_label = ifd_path_parm.parmTemplate().label()
            hqrop.displayError(" ".join(["The value of the", ifd_parm_label,
                               "parameter in\n", hou.pwd().path(), "\n"
                               "must not be blank."]))
            return False

    return True

def _submitRenderJob(parms):
    """Build and submit the top-level render job."""
    
    if parms["use_output_driver"]:
        hip_file, hfs = hqrop.getHipFileAndHFS(parms)
        if hip_file is None or hfs is None:
            return
    else:
        hfs = hqrop.getHFS(parms)
        if hfs is None:
            return

    # We submit a top-level job that doesn't do anything except wait for its
    # children to finish.  This job initially has a single child that we also
    # submit at the same time.  When we're generating IFDs, that child job
    # generates them and then submits render jobs as children of the top-level
    # job.  When we're not generating IFDs, that child will submit individual
    # render jobs to render each batch of frames directly from the hip file.
    
    if parms["batch_all_frames"]:
        frames_per_job = -1
    else:
        frames_per_job = parms["frames_per_job"]

    # Build the list of parameters to pass to the child job.
    hq_parms = {
        "frames_per_job": frames_per_job,
        "render_frame_order": parms["render_frame_order"],
        "dirs_to_create": parms["dirs_to_create"],
        "min_hosts_per_job": parms["min_hosts_per_job"],
        "max_hosts_per_job": parms["max_hosts_per_job"],
        "use_render_tracker" : parms["use_render_tracker"],
    }
    if parms["make_ifds"]:
        hq_parms.update({
            "ifd_path": parms["output_ifd"],
            "delete_ifds": parms["delete_ifds"]
        })
    elif parms["use_output_driver"]:
        # The render single tile option is only available 
        # when rendering from an output driver and not generating IFDs.
        hq_parms["render_single_tile"] = parms["render_single_tile"]

    if parms["use_output_driver"]:
        hq_parms["output_driver"] = parms["output_driver"]
        hq_parms["hip_file"] = hip_file
        hq_parms["project_name"] = _getProjectName(
            parms["hq_server"], hip_file)
    else:
        hq_parms.update({
            "ifd_path" : parms["ifd_path"],
            "start_frame" : parms["start_frame"],
            "end_frame" : parms["end_frame"],
            "frame_skip" : parms["frame_skip"],
            "project_name" : _getProjectName(
                parms["hq_server"], parms["ifd_path"])
        })

    # Determine number of cpus per job.
    # Zero means to use the maximum number of CPUs.
    cpus_per_job = 0
    if bool(parms["is_CPU_number_set"]):
        cpus_per_job = int(parms["CPUs_to_use"])

    # Now build the spec for the child job.
    apply_conditions_to_children = True
    if parms["make_ifds"]:
        script_name = "hq_make_ifds.py"
        command_type = "hythonCommands"
        child_job = {"name": "Generate IFDs"}

        # Set client conditions.
        assign_to = parms["assign_ifdgen_to"]
        if assign_to == "clients":
            child_job["host"] = parms["ifdgen_clients"]
            apply_conditions_to_children = False
        elif assign_to == "client_groups":
            child_job["hostgroup"] = parms["ifdgen_client_groups"]
            apply_conditions_to_children = False
    elif not parms["use_output_driver"]:
        script_name = "hq_prepare_ifd_render.py"
        command_type = "pythonCommands"
        child_job = {"name": "Prepare IFD Render Jobs"}
    else:
        script_name = "hq_submit_renders.py"
        command_type = "hythonCommands"
        child_job = {"name": "Prepare Render Jobs"}

    # Set the number of cpus in the child job spec.
    if cpus_per_job > 0:
        child_job["cpus"] = cpus_per_job
    else:
        child_job["tags"] = ["single"]

    # Build job commands.
    hq_cmds = hqrop.getHQueueCommands(hfs, cpus_per_job)
    if hq_cmds is None:
        return
    commands = hqrop.getJobCommands(hq_cmds, command_type, script_name)

    # Build the environment that the job will run in.
    env_vars = {
        "HQCOMMANDS": hutil.json.utf8Dumps(hq_cmds),
        "HQPARMS": hutil.json.utf8Dumps(hq_parms),
    }
    if len(parms["environment"]) > 0:
        env_vars["HQ_PRESERVE_ENV_VARS"] = ",".join(parms["environment"].keys())
        env_vars.update(parms["environment"])

    # Update job spec.
    child_job.update({
        "environment": env_vars,
        "priority" : parms["priority"],
        "command": commands
    })
    hqrop.setEnvironmentVariablesInJobSpec(child_job)
    
    if (parms["name"] != "<default>") and parms["name"]:
        name = parms["name"]
    elif parms["use_output_driver"]:
        name = "Render -> HIP: %s ROP: %s" % (hip_file, parms['output_driver'])
    else:
        name = 'Render -> IFDs: %s' % (parms["ifd_path"])

    # Build and submit the top-level job.
    main_job = hqrop.buildContainingJobSpec(
        name, hq_cmds, parms, child_job, apply_conditions_to_children)
    if cpus_per_job > 0:
        main_job["cpus"] = cpus_per_job
    else:
        main_job["tags"] = ["single"]
    hqrop.setEnvironmentVariablesInJobSpec(main_job)
    hqrop.sendJob(parms["hq_server"], main_job, parms["open_browser"])

def _byu_troubleshoot_hq(parms):
    """Build and submit the top-level render job."""
    
    if parms["use_output_driver"]:
        hip_file, hfs = hqrop.getHipFileAndHFS(parms)
        if hip_file is None or hfs is None:
            return
    else:
        hfs = hqrop.getHFS(parms)
        if hfs is None:
            return

    # We submit a top-level job that doesn't do anything except wait for its
    # children to finish.  This job initially has a single child that we also
    # submit at the same time.  When we're generating IFDs, that child job
    # generates them and then submits render jobs as children of the top-level
    # job.  When we're not generating IFDs, that child will submit individual
    # render jobs to render each batch of frames directly from the hip file.
    
    if parms["batch_all_frames"]:
        frames_per_job = -1
    else:
        frames_per_job = parms["frames_per_job"]

    # Build the list of parameters to pass to the child job.
    hq_parms = {
        "frames_per_job": frames_per_job,
        "render_frame_order": parms["render_frame_order"],
        "dirs_to_create": parms["dirs_to_create"],
        "min_hosts_per_job": parms["min_hosts_per_job"],
        "max_hosts_per_job": parms["max_hosts_per_job"],
        "use_render_tracker" : parms["use_render_tracker"],
    }
    if parms["make_ifds"]:
        hq_parms.update({
            "ifd_path": parms["output_ifd"],
            "delete_ifds": parms["delete_ifds"]
        })
    elif parms["use_output_driver"]:
        # The render single tile option is only available 
        # when rendering from an output driver and not generating IFDs.
        hq_parms["render_single_tile"] = parms["render_single_tile"]

    if parms["use_output_driver"]:
        hq_parms["output_driver"] = parms["output_driver"]
        hq_parms["hip_file"] = hip_file
        hq_parms["project_name"] = _getProjectName(
            parms["hq_server"], hip_file)
    else:
        hq_parms.update({
            "ifd_path" : parms["ifd_path"],
            "start_frame" : parms["start_frame"],
            "end_frame" : parms["end_frame"],
            "frame_skip" : parms["frame_skip"],
            "project_name" : _getProjectName(
                parms["hq_server"], parms["ifd_path"])
        })

    # Determine number of cpus per job.
    # Zero means to use the maximum number of CPUs.
    cpus_per_job = 0
    if bool(parms["is_CPU_number_set"]):
        cpus_per_job = int(parms["CPUs_to_use"])

    # Now build the spec for the child job.
    apply_conditions_to_children = True
    if parms["make_ifds"]:
        script_name = "hq_make_ifds.py"
        command_type = "hythonCommands"
        child_job = {"name": "Generate IFDs"}

        # Set client conditions.
        assign_to = parms["assign_ifdgen_to"]
        if assign_to == "clients":
            child_job["host"] = parms["ifdgen_clients"]
            apply_conditions_to_children = False
        elif assign_to == "client_groups":
            child_job["hostgroup"] = parms["ifdgen_client_groups"]
            apply_conditions_to_children = False
    elif not parms["use_output_driver"]:
        script_name = "hq_prepare_ifd_render.py"
        command_type = "pythonCommands"
        child_job = {"name": "Prepare IFD Render Jobs"}
    else:
        script_name = "hq_submit_renders.py"
        command_type = "hythonCommands"
        child_job = {"name": "Prepare Render Jobs"}

    # Set the number of cpus in the child job spec.
    if cpus_per_job > 0:
        child_job["cpus"] = cpus_per_job
    else:
        child_job["tags"] = ["single"]

    # Build job commands.
    hq_cmds = hqrop.getHQueueCommands(hfs, cpus_per_job)
    if hq_cmds is None:
        return
    commands = hqrop.getJobCommands(hq_cmds, command_type, script_name)

    # Build the environment that the job will run in.
    env_vars = {
        "HQCOMMANDS": hutil.json.utf8Dumps(hq_cmds),
        "HQPARMS": hutil.json.utf8Dumps(hq_parms),
    }
    if len(parms["environment"]) > 0:
        env_vars["HQ_PRESERVE_ENV_VARS"] = ",".join(parms["environment"].keys())
        env_vars.update(parms["environment"])

    # Update job spec.
    child_job.update({
        "environment": env_vars,
        "priority" : parms["priority"],
        "command": commands
    })
    hqrop.setEnvironmentVariablesInJobSpec(child_job)
    
    if (parms["name"] != "<default>") and parms["name"]:
        name = parms["name"]
    elif parms["use_output_driver"]:
        name = "Render -> HIP: %s ROP: %s" % (hip_file, parms['output_driver'])
    else:
        name = 'Render -> IFDs: %s' % (parms["ifd_path"])

    # Build and submit the top-level job.
    main_job = hqrop.buildContainingJobSpec(
        name, hq_cmds, parms, child_job, apply_conditions_to_children)
    if cpus_per_job > 0:
        main_job["cpus"] = cpus_per_job
    else:
        main_job["tags"] = ["single"]
    
    hqrop.setEnvironmentVariablesInJobSpec(main_job)

    fname = os.path.expandvars('${JOB}/tmp/hq_jobs_troubleshoot.log')

    fp = open(fname, 'a')
    fp.write('\n\nWriting log for job "' + main_job['name'] + '" at ' + str(datetime.now()) + ':\n')
    json.dump(main_job, fp, indent=4)
    fp.close()

    hqrop.sendJob(parms["hq_server"], main_job, parms["open_browser"])

def _getProjectName(hq_server_url, hip_path):
    # If we've been submitted from another HQueue job, as is the case when
    # rendering in the cloud, check $HQPARMS to see if the project name
    # was set.  Otherwise, use the render tracker to choose a unique project
    # name.
    if "HQPARMS" in os.environ:
        parms = hutil.json.utf8Loads(os.environ["HQPARMS"])
        if "project_name" in parms:
            return parms["project_name"]

    project_name = rendertracker.applyProjectNameFormula(
        hutil.username.currentUserName(), hip_path)

    # Now connect to the render tracker to get a unique project name.
    render_tracker_rpc = rendertracker.getConnection(
        hqrop.getHQueueServerMachineFromURL(hq_server_url))
    if render_tracker_rpc is not None:
        project_name = render_tracker_rpc.suggestInactiveProjectName(
            project_name)
    return project_name


# Note that __name__ is not "__main__" when invoked from soho.
# __name__ is not "HQrender" when it is invoked from soho but it is when
# imported as a module
if __name__ != "HQrender":
    render()

