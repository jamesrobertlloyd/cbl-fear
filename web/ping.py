import subprocess
import numpy as np

machines = ['felafel',
          'few',
          'fence',
          'feckless',
          'fetlock',
          'feudal',
          'fez',
          'felicity',
          'feature',
          'fever']

# machines = ['felafel',
#             'few',
#             'fence']

# Ping the cluster

pings = -np.ones(len(machines))

for (i, machine) in enumerate(machines):
    print 'Pinging %s' % machine
    ping_response = subprocess.Popen(["/bin/ping", "-c5", machine], stdout=subprocess.PIPE).stdout.read().split('\n')
    if ping_response[-2][:3] == 'rtt':
        print 'Success :D'
        pings[i] = float(ping_response[-2].split('/')[4])
    else:
        print 'Failure D:'

# Sort the pings - determine which are dead

idx = np.argsort(-pings)

sorted_pings = pings[idx]
sorted_machines = []
for i in idx:
    sorted_machines.append(machines[i])

dead = sorted_pings == -1

# Create some csvs of the data

dead_list = 'Machine,\n'
ping_list = 'Machine,Ping\n'

for (machine, is_dead, ping) in zip(sorted_machines, dead, sorted_pings):
    if is_dead:
        dead_list += machine + ',\n'
    else:
        ping_list += '%s,%f\n' % (machine, ping)

# Remove trailing new lines and save

dead_list = dead_list[:-1]
ping_list = ping_list[:-1]

with open('ping.csv', 'w') as f:
    f.write(ping_list)

with open('dead.csv', 'w') as f:
    f.write(dead_list)