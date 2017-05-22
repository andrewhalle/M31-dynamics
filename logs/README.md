To get data out of our simulations, log files (.log) were saved at regularly spaced intervals using the method `save` of the `Simulation` class from `REBOUND`. These log files are available in `suite`. These files are binary files, and so will only work for Ubuntu users. For Ubuntu users, the Python code to restore a simulation log is
'''python
import rebound
sim = rebound.Simulation.from_file(path_to_log)
'''

In an effort to make this code available to all, this repository also includes universal log files (.logu) in `suite_u`. This files are ASCII files with the pertinent information to regenerate the `Simulation` object. Code to produce and use these logs files is available in `../scripts/incude/universal_logs.py`. The code to restore a universal simulation log is (this code is written as if you are running code from the `../figures/scripts` directory. The argument to `sys.path.append` should be changed accordingly if this is not the case)
'''python
import sys
sys.path.append("../include")
from universal_logs import *
sim = restore(path_to_logu)
'''
