import subprocess
import numpy as np

import cblparallel.pyfear

# Load list of dead machines

with open('../data/dead-ping.csv', 'r') as f:
    machines_ping = [line.strip().strip(',') for line in f]
with open('../data/dead-ssh.csv', 'r') as f:
    machines_ssh = [line.strip().strip(',') for line in f]

dead_machines = set(machines_ping + machines_ssh)

# Connect to fear

with cblparallel.pyfear.fear() as fear:

    # Check for any jobs listed on qstat on dead machines

    queue_list = fear.qstat_xml()
    stranded_users = []

    for queue in queue_list:
        for job in queue:
            # Iterate over fields in job - extracting user and machine
            for element in job:
                if element.tag == 'JB_owner':
                    user = element.text
                elif element.tag == 'queue_name':
                    try:
                        machine = element.text.split('@')[-1].split('.')[0]
                    except:
                        machine = ''
            # Append user if machine is dead
            if machine in dead_machines:
                stranded_users.append(user)
    stranded_users = list(set(stranded_users))

    # Turn into csv

    dead_list = 'User,\n'

    for user in stranded_users:
        dead_list += user + ',\n'

    # Remove trailing new lines and save

    dead_list = dead_list[:-1]

    with open('../data/dead-users.csv', 'w') as f:
        f.write(dead_list)

    print 'Death toll calculated'