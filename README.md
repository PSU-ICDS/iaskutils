# Table of Contents

* [Overview](#overview)
* [Installation](#installation)
* [Accessing Documentation](#accessing-documentation)
* [Bug Reporting and Requesting Features](#bug-reporting-and-requesting-features)
* [Contributing Guidelines](#contributing-guidelines)
* [License](#license)
* [Troubleshooting](#troubleshooting)

# Overview

Welcome to the **iaskutils** GitHub repository!

![Demonstration](./share/gifs/demo.gif)

You might be asking yourself, "what is a iaskutils collection?" Well, it is just a collection of various scripts and tools used by the [Penn State ICDS i-ASK helpdesk](https://www.icds.psu.edu/computing-services/support/) to help the users of the Roar supercomputer. The iaskutils collection is ever growing, but here is a list of the tools currently available in the collection:

* **`collector`:** A simple script to collect information about your environment.
* **`gathero`:** A script to collect essential information about a user's job(s).
* **`relinkworkscratch`:** A simple script to reestablish the work and scratch directory symlinks in a user's home directory.
* **`setupcomsolsymlink`:** A simple script to relocate the COMSOL cache to the work directory.
* **`setupcondasymlink`:** A simple script to relocate the conda cache to the work directory.

To get access to the collection on the Roar cluster, you simply just need to use the following commands:

```bash
$ module use /gpfs/group/dml129/default/sw7/modules
$ module load iaskutils/1.2
```

Now let's get onto the meat of this README!

# Installation

1. [Environment setup](#environment-setup)
2. [Installing collector](#installing-collector)
3. [Installing gathero](#installing-gathero)
4. [Installing relinkworkscratch](#installing-relinkworkscratch)
5. [Installing setupcomsolsymlink](#installing-setupcomsolsymlink)
6. [Installing setupcondasymlink](#installing-setupcondasymlink)
7. [Set up the iaskutils module file](#set-up-the-iaskutils-module-file)

## Environment setup

First, in order to use the **iaskutils** collection, you need to set up the environment by installing the necessary prerequisites. Luckily, you only need to use the following commands on the Roar cluster:

```bash
$ module load anaconda3/2020.07
$ conda create --prefix /gpfs/group/dml129/default/sw7/python python=3.9
$ export PATH=/gpfs/group/dml129/default/sw7/python/bin:$PATH
$ cd /gpfs/group/dml129/default/sw7
$ git clone https://github.com/ICDS-Roar/iaskutils.git
$ cd iaskutils
$ pip install -r requirements.txt
$ pip install pyinstaller
$ mkdir bin
```

Now that the iaskutils environment is ready to go, it is now time time to install each of the tools. Let's start with **collector**!

## Installing collector

To install collector, you simply need to use `pyinstaller` and then set up a symlink to the `/bin` directory we created (just make sure that you are still in the iaskutils directory!):

```bash
$ pyinstaller collector.py
$ ln -s $(pwd)/dist/collector/collector $(pwd)/bin/collector
```

Now that collector is done, onto **gathero**!

## Installing gathero

Like collector, the install process for gathero is the same:

```bash
$ pyinstaller gathero.py
$ ln -s $(pwd)/dist/gathero/gathero $(pwd)/bin/gathero
```

If you haven't deduced it already, the install process for the rest of the Python scripts in the collector is virtually the same!

## Installing relinkworkscratch

```bash
$ pyinstaller relinkworkscratch.py
$ ln -s $(pwd)/dist/relinkworkscratch/relinkworkscratch $(pwd)/bin/relinkworkscratch
```

## Installing setupcomsolsymlink

```bash
$ pyinstaller setupcomsolsymlink.py
$ ln -s $(pwd)/dist/setupcomsolsymlink/setupcomsolsymlink $(pwd)/bin/setupcomsolsymlink
```

## Installing setupcondasymlink

```bash
$ pyinstaller setupcondasymlink.py
$ ln -s $(pwd)/dist/setupcondasymlink/setupcondasymlink $(pwd)/bin/setupcondasymlink
```

## Set up the iaskutils module file

Now, in order for users and i-ASK teamates alike to access the iaskutils collection on Roar, you need to set up the corresponding module file. Luckily, you only need to use the following commands to set up the module file:

```bash
$ cd /gpfs/group/dml129/default/sw7
$ mkdir -p modules/iaskutils
$ cp iaskutils/share/modules/1.2.lua modules/iaskutils/1.2.lua
$ chmod -R ugo+rx iaskutils
$ chmod -R ugo+rx modules
```

Now you should be able to load the iaskutils collection by using the following commands:

```bash
$ module use /gpfs/group/dml129/default/sw7/modules
$ module load iaskutils/1.2
```

**Congratulations!** You have succesfully installed the iaskutils collection!

# Accessing Documentation

The nice thing about the iaskutils collection is that each of the scripts/tools included has a corresponding man page to go with it! For example, here is how you would retrieve the man page for **gathero**:

```bash
$ module use /gpfs/group/dml129/default/sw7/modules
$ module load iaskutils/1.2
$ man gathero
```

If man pages are not your style, you can access the PDF documentation for each of the scripts in the `/share/doc` directory of this repository.

# Bug Reporting and Requesting Features

* [Reporting Bugs](#reporting-bugs)
* [Requesting Features](#requesting-features)

## Reporting Bugs

If you encounter any bugs or any *oddities* when working with the iaskutils collection, please open an issue on this repository. In that issue, please include the following sections:

1. Which script are you using?
2. What are you trying to accomplish?
3. The stacktrace of the error you are receiving.

The more information the better. We cannot fix the problem if we do not know how it is being caused. Also, when you open the issue, please label the issue as a **bug**.

## Requesting Features

If there is a new tool or feature you would like to see added to this collection, please open an issue on this repository. While we cannot promise that every feature requested will be added, we will at least give it a look! Also, when requesting a feature as an issue, please label the issue as a **feature request** or **enhancement**.

# Contributing Guidelines

If you would like to help us add to the iaskutils collection by either fixing issues, adding new tools, or even porting to another cluster, please create a fork of this repository. In that fork, create a branch that alludes to what you are trying to accomplish.

After completing the work in your branch, please open a pull request to the main repository. In your pull request, please include the following things:

1. What did you add/modify in your branch?
2. Why did you make the addition/modification?

Once again, the more information you include the better! Once we review the pull request, we will determine if it should be merged or not! If we say no, we will comment why.

# License

![License](https://img.shields.io/badge/license-MIT-brightgreen)

This repository is licensed under the permisive MIT License. For more information on what this license entails, please feel free to visit https://en.wikipedia.org/wiki/MIT_License.

# Troubleshooting

If you encounter any issues while using any of the scripts contained in the iaskutils collection on the Roar cluster then please open an issue, or contact Jason at the ICDS i-ASK center at either iask@ics.psu.edu or jcn23@psu.edu.
