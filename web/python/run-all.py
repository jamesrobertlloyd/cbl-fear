import subprocess
import os
import time

# Runs all fear related scripts

while True:

    print '\n* * * * *\nAcquiring kittens\n* * * * *\n'

    #saved_path = os.getcwd()
    #os.chdir('../feature-generation/')
    subprocess.call(['python', 'kittens.py'])
    #os.chdir(saved_path)

    print '\n* * * * *\nPinging cluster\n* * * * *\n'

    subprocess.call(['python', 'ping.py'])

    print '\n* * * * *\nQuerying CPU usage\n* * * * *\n'

    subprocess.call(['python', 'cpu.py'])

    print '\n* * * * *\nCheck for stranded jobs\n* * * * *\n'

    subprocess.call(['python', 'dead-jobs.py'])

    print '\n* * * * *\nRecording update time\n* * * * *\n'

    the_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    with open('../data/time.csv', 'w') as f:
        f.write(the_time)

    print 'Nap time!'
    time.sleep(5*60)