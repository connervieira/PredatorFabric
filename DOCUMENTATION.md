# Documentation

This document explains how to install, set-up, and use Predator Fabric.


## Introduction

Predator Fabric works extremely similar to traditional Predator, in that it analyzes license plates in a cycle process.

1. An image is captured.
2. The image is processed according to the configuration.
3. The image is analyzed by an ALPR back-end.
4. Results are filtered and processed.
5. If valid plates were detected, the results are forwarded off to a configured remote service.
6. If configured to do so, the image used for analysis may also be forwarded off to a configured remote service.


## Installation

Note that the dependencies for Predator and Predator Fabric are effectively identical. If you've already installed and set-up vanilla Predator, you should be able to download and run Predator Fabric without installing any prerequisites.

1. Install Python
    - Example: `sudo apt-get install python3 python3-pip`
2. Install the required Python libraries
    - Example: `pip3 install psutil requests`
3. Install a supported ALPR engine, like [Phantom](https://v0lttech.com/phantom.php)
    - After installation, you should be able to run the executable with the `alpr` command. Otherwise, Predator Fabric will not be able to start the ALPR process.
4. Copy the Predator Fabric directory to any accessible location on your system.
    - Example: `cp -r ~/Downloads/PredatorFabric ~/Software/PredatorFabric`
    - The main Predator Fabric directory, containing all of the scripts and support files, is referred to as the "root instance" or "root Predator Fabric" directory.


## Set-up

After completing the installation process, you can begin the set-up process.

1. Create a "working directory", and specify its absolute path in the configuration.
    - The working directory is where Predator Fabric will store files it is actively working with.
2. Create an "interface directory", and specify its absolute path in the configuration.
    - The interface directory is where Predator Fabric stores files used to communicate with external local services.
3. Configure Predator Fabric as desired.
    - The configuration process is described in the [CONFIGURATION.md](CONFIGURATION.md) document.


## Usage

Once Predator Fabric is ready, you can run it using Python3. For example, you might use the command `cd ~/Software/PredatorFabric; python3 main.py` when the root Predator Fabric directory is located at `~/Software/PredatorFabric`.

Predator can also be started and managed graphically using Cortex.


## Integration

Predator Fabric is not intended to operate as a stand-alone system, and instead feeds information to an external service. To learn more about integrating with external services, see the [INTEGRATION.md](INTEGRATION.md)
