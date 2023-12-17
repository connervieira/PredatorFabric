# Configuration

This document describes the configuration values found `config.json`.


## General

This section contains settings that effect general operation.

- `name` sets the name of the platform, for branding purposes.
- `start_message` sets a message that will be displayed when the program starts.
- `interval` defines a fixed delay, in seconds, at the beginning of each loop.


## Image

This section contains settings regarding image processing.

- `camera` contains camera related configuration options.
    - `provider` determines which back-end will be used to capture images. Currently, `"fswebcam"` and `"imagesnap"` are supported. Setting this value to `"off"` will disable image capture, for sake of debugging.
    - `device` determines which camera device the camera back-end will use to capture images.
    - `resolution` determines the camera resolution that will be used to capture images. This value is only supported by FSWebcam, and will be ignored by ImageSnap.
    - `arguments` contains custom command line arguments that will be attached to the camera back-end execution command. If you want to directly customize camera operation, this allows you to do so.
    - `file_name` is a string that determines the file name used for the images captured by the camera back-end.
- `processing`
    - `cropping`
        - `enabled` is a boolean value that determines whether image cropping is enabled or disabled. If you don't plan on using image cropping, you should set this to 'false' to increase efficiency.
        - `left_margin` is an integer number determines how many pixels will be cropped from the left side of the image.
        - `right_margin` is an integer number determines how many pixels will be cropped from the right side of the image.
        - `top_margin` is an integer number determines how many pixels will be cropped from the top side of the image.
        - `bottom_margin` is an integer number determines how many pixels will be cropped from the bottom side of the image.
    - `rotation`
        - `enabled` is a boolean value that determines whether image rotation is enabled or disabled. If you don't plan on using image rotation, you should set this to 'false' to increase efficiency.
        - `angle` is an integer determines the angle, in degrees clockwise, that the image will be rotated.


## ALPR

This section contains settings regarding the license plate recognition process.

- `engine` determines which ALPR processing engine will be used. Currently, only `"openalpr"` and `"phantom"` are supported.
- `guesses` is an integer that defines how many guesses will be made as to the characters of each license plate.
- `confidence` is an integer between `0` and `100` that defines the minimum confidence percentage for a guess to be considered viable. Results below this confidence level will be thrown out.


## Network

This section contains settings that control how information will be shared with network services.

- `identifier` sets a unique identifier that can be used to authenticate and communicate with network services.
- `results_submission` contains settings relating to the submission of local ALPR processing results.
    - `target` defines the network address that processing information will be submitted to.
    - `mode` specifies the mode in which local ALPR results are submitted. This can be set to `"off"` to disable the submission of local processing results, `"auto"` to submit information only when license plates are detected by the local processing system, or `"on"` to always upload processing results.
- `remote_processing` contains settings relating to the submission of images to a remote processing service.
    - `target` is an optional value that sets a network address that encoded image information will be submitted to.
    - `mode` specifies the mode in which remote processing information is submitted. This can be set to `"off"` to disable remote processing, `"auto"` to submit images where license plates were detected by the local processing system, or `"on"` to always submit captured images regardless of the local processing system results.


## Developer

This section contains settings that allow technical users to debug, repair, and modify the platform.

- `debug_mode` is a boolean value that enables verbose system messages, and disables console clearing. This makes it possible to see exactly what tasks are being completed at any given moment, and how long they take to complete.
- `working_directory` is a string that defines where active files will be stored.
- `interface_directory` is a string that defines where files related to interacting with a front-end interface will be stored.
- `print_alpr_diagnostics` is a boolean value that defines whether the ALPR engine response data will be printed to the console for debugging purposes.
- `max_heartbeat_history` is an integer that determines how many 'pulses' will be stored in the heartbeat log before they are trimmed.
- `max_plate_history_age` is an integer that determines how long, in seconds, outputs in the plate history will be retained before being discarded.
- `ignore_list` contains settings regarding ignore-list functionality.
    - `enabled` is a boolean that enables or disables custom license plate ignore lists. This is useful if you want to temporarily disable custom configured ignore lists for some reason.
    - `local_file` is the name of a JSON file in the working directory that contains a list of license plates that should be ignored. This can be useful if you want to prevent common vehicles, like maintainence trucks, from being processed, to keep logs organized. This can also be a way to prevent the license plates of privacy-concerned customers from being logged.
    - `remote_sources` is a list of URLs to be used remote ignore-list sources. These are optional, but allow administrators to remotely issue ignore lists to multiple Predator instances from a central server.
