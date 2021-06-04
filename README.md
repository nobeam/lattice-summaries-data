# Lattice Summaries - NoBeam Data

This repository is used to manage the lattice/input files for the [lattice-summaries](https://github.com/nobeam/lattice-summaries) instance hosted at https://lattice-summaries.netlify.app. Every time a new lattice file is pushed to this repository, it automatically gets converted into serval lattice file formats. The resulting lattice files and simulation results are pushed to the [lattice-summaries-results](https://github.com/nobeam/lattice-summaries-results) repository.

## Add a new Lattice

1. Clone this repository
2. Create a new branch (e.g. `goslawski/add-mls2-lattice`)
3. Check if your lattice file meets all the requirements. [(see lattice file requirements)](#lattice-file-requirements) 
4. Add your lattice file to the `originals/<namespace>` folder. [(see naming scheme)](#naming-scheme)
5. Add an entry in the `info.toml` file. [(see below)](#infotoml)
6. Commit your changes to your new branch.
    - The commit summary should be `add goslawski/mls2_<family>_v_<version>` for a newly added lattice.
    - The commit summary should be `update goslawski/mls2_<family>_v_<version>` in case a lattice file is updated.
7. Push your branch and create a [pull request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
    - All pull request must be reviewed by someone else before merged.
    - All pull request must be squash merged. 

### info.toml

Meta information on the lattices is listed in the `info.toml` file. If you add a new lattice to this repo don't forget to add an entry to this file: 

```toml
# example entry

[mls2_scaled-from-bessy2_v_1]
title = "mls2 based on bessy2"
machine = "mls2"
authors = ["Goslawski", "Max Mustermann"]
energy = 1200
simulations = ["apace", "elegant", "madx"]
labels = []
description = """
A possible design lattice for the MLS2 based on a scaled down version of BESSY 2
"""
```

Most of the attributes should be self-explanatory. A list of available labels is listed below:

> :memo: TODO@michael: add list of useful labels
