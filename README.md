This is the repository for code pertaining to [Madigan, et. al. 2017](https://arxiv.org/abs/1705.03462).

## About
Eccentric nuclear disks have long been thought to be responsible for asymmetric galactic nuclei. Our closest neighbor, the Andromeda Galaxy, contains a double nucleus which was originally thought to be a star cluster merging with the galactic center. Later evidence showed that these two brightness peaks were made up of the same types of stars, and so had to be the same stellar population.
What has been missing from this explanation is a method to stabilize this eccentric nuclear disk. We see evidence for asymmetric nuclei in a sizeable percentage of galaxies, so this ought to be a stable structure. We show in this paper, via *N*-body simulations, a new dynamical mechanism for stability of eccentric nuclear disks.

## About the code
To accomplish these *N*-body simulations, we use the Python package [`REBOUND`](https://github.com/hannorein/rebound) (v. 2.15.0) to simulate 100 particles orbiting a supermassive black hole. The central black hole is 100 times more massive than the disk of stars surrounding it.
This code also relies upon the [`matplotlib`](https://github.com/matplotlib/matplotlib) (v. 1.5.3) and [`numpy`](https://github.com/numpy/numpy) (v. 1.11.1) packages for data analysis.

## Running
The simplest way to run this code is to make use of the scripts `make_directory_structure.sh` and `scripts/figures/gen_all_figures.py`. `make_directory_structure.sh` creates the images directories that the data analysis scripts depend on. `gen_all_figures.py` runs all figure-producing code. This script should take some time to run and should populate the image directory with the figures. `make_directory_structure.sh` should be run first.
