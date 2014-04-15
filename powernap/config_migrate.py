#!/usr/bin/env python
#
# Script to migrate a v1.7 configuration file to a v1.xx configuration
# file

import os, sys

# Parse command line
if len(sys.argv) != 4:
  print 'Usage :- %s old_config old_action new_config' % sys.argv[0]
old_cnf_path = sys.argv[1]
old_act_path = sys.argv[2]
new_cnf_path = sys.argv[3]

# Load OLD config
try:
  execfile(old_cnf_path)
except Exception, e:
  print 'ERROR: failed to load old configuration [e=%s]' % e
  sys.exit(1)

# Process new config file
lines = []
try:
  fp = open(new_cnf_path, 'r')
  for l in fp.readlines():
    l = l.strip()

    # Ignore blank, comment and section line
    if not l or l[0] in [ '#', '[' ]:
      lines.append(l)
   
    # Interval
    elif l.startswith('interval'):
      lines.append('interval = %0.2f' % INTERVAL_SECONDS)

    # Absent
    elif l.startswith('absent'):
      lines.append('absent = %0.2f' % ABSENT_SECONDS)
 
    # Grace
    elif l.startswith('grace'):
      lines.append('grace = %0.2f' % GRACE_SECONDS)

    # Debug
    elif l.startswith('debug'):
      lines.append('debug = %d' % DEBUG)
  
    # Action
    elif l.startswith('action_enter_sleep'):
      if os.access(old_act_path, os.X_OK):
        lines.append("action_enter_sleep = '%s'" % os.path.abspath(old_act_path))
      else: lines.append(l)

    # Monitors
    elif l.startswith('monitors'):
      monitors = "monitors = [ \"InputMonitor()\""
      for m in MONITORED_PROCESSES:
        monitors += ", \"ProcessMonitor({'regex':'%s'})\"" % m
      monitors += " ]"
      lines.append(monitors)

    # All else
    else: lines.append(l)
  fp.close()

  # Store data
  fp = open(new_cnf_path, 'w')
  for l in lines:
    fp.write(l + '\n')
  fp.close()
except Exception, e:
  print 'ERROR: failed to update configuration [e=%s]' % e
  sys.exit(1)

# Done
print 'Configuration successfully updated'
