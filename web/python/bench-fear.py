import scipy.io
import os
from time import gmtime, strftime
import time

import cblparallel

while True:

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
		benchmarks = benchmarks[0] + benchmarks[-499:]

	# Append to results

	benchmarks.append('%s,%f,%s\n' % (the_time, t, name))

	with open('../data/bench.csv', 'w') as f:
		f.writelines(benchmarks)

	print 'Nap time'
	time.sleep(30 * 60)