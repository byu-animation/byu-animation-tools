import time
import xmlrpclib

# Connect to the HQueue server.
hq_server = xmlrpclib.ServerProxy( "http://hqueue:5000")

# Define a job which renders an image from an IFD using Mantra.
job_spec = { 
         "name":	 "Render My Image",
         "shell":	 "bash",
         "command": 
                  "cd $HQROOT/houdini_distros/hfs;"
                  + " source houdini_setup;"
                  + " mantra < $HQROOT/path/to/ifds/some_frame.ifd"
}

# Submit the job to the server.
# newjob() returns a list of job ids (in case multiple jobs are passed in at once).
job_ids = hq_server.newjob(job_spec)

# Periodically check the job progress and status.
while True:
         # Get the job status. 
         job_details = hq_server.getJob(job_ids[0], [ "progress", "status"])
         status = job_details["status"] 

         # Check if the job is finished. 
         if status in ("succeeded", "failed", "cancelled", "abandoned"):
                  break

         # Job is not finished. Output its progress. 
         progress = job_details["progress"]          print "Progress: %.2f" % (progress * 100) 

# Output final status. 
print "Status: ", job_details["status"]