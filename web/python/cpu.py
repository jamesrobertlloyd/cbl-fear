import subprocess
import numpy as np
import pysftp

from cblparallel.config import * # Various constants such as USERNAME

# Load list of machines

with open('../data/machines.csv', 'r') as f:
    machines = [line.strip() for line in f]

# Ask each machine how much CPU is being used

cpus = -np.ones(len(machines))

for (i, machine) in enumerate(machines):
    try:
        machine_connection = pysftp.Connection(host=machine, private_key=LOCAL_TO_REMOTE_KEY_FILE)
        top_response = machine_connection.execute('top -bn2 -p1')
        for line in reversed(top_response):
            if line[:3] == 'Cpu':
                relevant_line = line
                break
        cpu = sum(float(text[-8:-3]) for text in relevant_line.strip().split(',') if text[-2:] == 'us')
        cpus[i] = cpu
        machine_connection.close()
        print 'CPU usage on %s is %f%%' % (machine, cpu)
    except:
        print 'Could not connect to %s' % machine

# Sort the cpus - determine which are dead

idx = np.argsort(-cpus)

sorted_cpus = cpus[idx]
sorted_machines = []
for i in idx:
    sorted_machines.append(machines[i])

dead = sorted_cpus == -1

# Create some csvs of the data

dead_list = 'Machine,\n'
cpus_list = 'Machine,CPU usage\n'

for (machine, is_dead, cpu) in zip(sorted_machines, dead, sorted_cpus):
    if is_dead:
        dead_list += machine + ',\n'
    else:
        cpus_list += '%s,%f\n' % (machine, cpu)

# Remove trailing new lines and save

dead_list = dead_list[:-1]
cpus_list = cpus_list[:-1]

with open('../data/cpus.csv', 'w') as f:
    f.write(cpus_list)

with open('../data/dead-ssh.csv', 'w') as f:
    f.write(dead_list)