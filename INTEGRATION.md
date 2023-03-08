# Integration

Predator Fabric is designed to be a network service that feeds information to another service. The information here explains how to integrate Predator Fabric with a custom service.


## Introduction

Predator Fabric shares information with external services both locally and over a network.

### Local

Predator Fabric shares information to local programs using the "interface" directory. This directory contains files that are updated as the program runs. These files allow external programs to read real-time information from Predator Fabric.

To learn more about integrating local programs with Predator Fabric, see the [INTEGRATION_LOCAL.md](INTEGRATION_LOCAL.md) document.

### Remote

Predator Fabric can send information about the results of local ALPR processing, as well as the raw captured image itself. These two processes are separate, but similar.

To learn more about receiving processed results, see the [INTEGRATION_RESULTS.md](INTEGRATION_RESULTS.md) document.
To learn more about receiving image data, see the [INTEGRATION_IMAGE.md](INTEGRATION_IMAGE.md) document.
