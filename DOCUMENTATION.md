# Documentation

This document explains how to install, set-up, and use Predator Fabric.


## Introduction

Predator Fabric works extremely similar to vanilla Predator, in that it analyzes license plates in a cycle process.

1. An image is captured.
2. The image is processed according to the configuration.
3. The image is analyzed by an ALPR back-end.
4. Results are filtered and processed.
5. If valid plates were detected, the results are forwarded off to a configured remote service.
6. If configured to do so, the image used for analysis may also be forwarded off to a configured remote service.


## Installation

1. Install the required Python libraries
    - Example: `pip3 install psutil requests`
