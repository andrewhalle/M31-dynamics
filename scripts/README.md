Code in this directory is broken into three folders.
## include
This folder contains utilities used by multiple scripts in the `figures folder`.
* `andrew_OrbitPlot.py` is a copy of the `REBOUND` script `OrbitPlot` with added features for coloring orbits.
* `universal_logs.py` contains code for generating and restoring universal logs.
* `M31config.py` contains the `Config` class for using data in `.config` files in the `figures` folder.
* `disk_splitter_include.py` contains the disk_splitter utility used by some code in `figures`.

## figures
This folder contains the code used to analyze the data from our simulations and produce figures. The main script in this folder is `gen_all_figures.py` which runs all scripts. `.config` files in this folder help the user interact with these tools without having to edit the scripts themselves. More entries can be added to the config file (for any element you may wish to interact with in the script) as long as the script is changed accordingly (using the other config/script pairs as example, this shouldn't be difficult).

## simulations
This folder contains the code to actually produce the simulations. Shouldn't need to be run, as we already have an extensive suite of log files available in this repository, with eccentric disks of a variety of initial eccentricities. If you do wish to run this code, it may need to be updated to fit the directory structure of this repository (which has been changed since the origial simulation integration).
