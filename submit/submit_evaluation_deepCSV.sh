executable              = $ENV(BTVHLTToolsDirectory)/submit/job_evaluation_deepCSV.sh
arguments               = $(ClusterId)$(ProcId)
output                  = $ENV(TrainingOutput)/htcondor_logs/evaluation_deepCSV_sing.$(ClusterId).$(ProcId).out
error                   = $ENV(TrainingOutput)/htcondor_logs/evaluation_deepCSV_sing.$(ClusterId).$(ProcId).err
log                     = $ENV(TrainingOutput)/htcondor_logs/evaluation_deepCSV_sing.$(ClusterId).log
should_transfer_files   = YES
getenv = True
when_to_transfer_output = ON_EXIT
request_GPUs = 1
request_CPUs = 1
Request_Memory = 16 Gb
+RequestRuntime = 36000
queue

