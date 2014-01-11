import subprocess
import os

# Runs all fear related scripts

print '\n* * * * *\nAcquiring kittehs\n* * * * *\n'

#saved_path = os.getcwd()
#os.chdir('../feature-generation/')
subprocess.call(['python', 'kittens.py'])
#os.chdir(saved_path)

print '\n* * * * *\nPinging cluster\n* * * * *\n'

#saved_path = os.getcwd()
#os.chdir('../feature-generation/')
subprocess.call(['python', 'ping.py'])
#os.chdir(saved_path)

print '\n* * * * *\nQuerying CPU usage\n* * * * *\n'

#saved_path = os.getcwd()
#os.chdir('../feature-generation/')
subprocess.call(['python', 'cpu.py'])
#os.chdir(saved_path)