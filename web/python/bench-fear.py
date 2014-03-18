import scipy.io
import os
from time import gmtime, strftime
import time
import zipfile, zlib
import sys

from cblparallel import pyfear
from cblparallel.config import *
import cblparallel
from cblparallel.util import mkstemp_safe

need_to_reload = False

while True:

    try:

        if need_to_reload:
            reload(pyfear) # In case fear connection has died
            need_to_reload = False

        # Send some benchmark code to the cluster

        BENCHMARK_CODE = r"""
        t = bench_no_graphics(5);
        name = getComputerName;
        save('%(output_file)s', 't', 'name');
        """

        scripts = [BENCHMARK_CODE]
        output_file = cblparallel.run_batch_on_fear(scripts, language='matlab', max_jobs=1000, verbose=False, zip_files=False, bundle_size=1)[0]

        # Read in results

        data = scipy.io.loadmat(output_file)
        t = data['t'][0,0]
        name = str(data['name'][0])
        os.remove(output_file)

        the_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        # Open results

        with open('../data/bench.csv', 'r') as f:
            benchmarks = f.readlines()

        if len(benchmarks) > 500:
            benchmarks = [benchmarks[0]] + benchmarks[-499:]

        # Append to results

        benchmarks.append('%s,%f,%s\n' % (the_time, t, name))

        with open('../data/bench.csv', 'w') as f:
            f.writelines(benchmarks)

        # Now time how long it takes to send, unzip and remove 50 files on fear

        temp_dir = LOCAL_TEMP_PATH  
        temp_files = [mkstemp_safe(temp_dir, '.txt') for i in range(50)]
        for temp_file in temp_files:
            with open(temp_file, 'w') as f:
                f.write('test text')
        print 'Zipping files'
        zip_file_name = mkstemp_safe(temp_dir, '.zip')
        zf = zipfile.ZipFile(zip_file_name, mode='w')
        for temp_file in temp_files:
            zf.write(temp_file, arcname=(os.path.split(temp_file)[-1]), compress_type=zipfile.ZIP_DEFLATED)
        zf.close()

        with pyfear.fear(via_gate=(LOCATION=='home')) as fear:
            # Start timing
            t1 = time.time()

            fear.copy_to_temp(zip_file_name)
            print 'Unzipping on fear'
            fear.command('cd %(temp_path)s ; unzip %(zip_file)s ; rm %(zip_file)s' % {'temp_path' : REMOTE_TEMP_PATH, 'zip_file' : os.path.split(zip_file_name)[-1]})
            print 'Finished unzipping'

            for temp_file in temp_files:
                fear.rm(os.path.join(REMOTE_TEMP_PATH, os.path.split(temp_file)[-1]))
            # Stop timing
            t2 = time.time()
            t = t2 - t1
            the_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        print 'Files removed remotely'
        for temp_file in temp_files:
            os.remove(temp_file)
        os.remove(zip_file_name)
        print 'Files removed locally'

        with open('../data/bench-zip.csv', 'r') as f:
            benchmarks = f.readlines()

        if len(benchmarks) > 500:
            benchmarks = [benchmarks[0]] + benchmarks[-499:]

        # Append to results

        benchmarks.append('%s,%f\n' % (the_time, t))

        with open('../data/bench-zip.csv', 'w') as f:
            f.writelines(benchmarks)


        print 'Nap time'
        time.sleep(30 * 60)

    except:

        print 'Oh no, I died!'
        print sys.exc_info()[0]
        need_to_reload = True
        time.sleep(30*60)