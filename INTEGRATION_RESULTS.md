# Results Receiving

This document explains how to integrate Predator Fabric with a receiver system.

These instructions explain the process of handling results sent by Predator Fabric. For information regarding image receiving, see the [INTEGRATION_IMAGE.md](INTEGRATION_IMAGE.md) document.


## Structure

### Overview

The data sent by Predator Fabric to the remote service follows this structure.

- "info" contains information regarding this data sample.
    - "identifier" is a string that contains an identifier set in the Predator Fabric configuration. This value is intended to be used like an API key, and to be used to authenticate a particular device before handling data received from it.
    - "timezone" is a list that contains time zone information from the sending device. This list should contain two strings representing a timezone with and without daylight savings.
    - "system" is a dictionary containing information about the system Predator Fabric is running on.
        - "python_version" contains information regarding the version of Python the system is using. This value takes the format of 3 numbers separated by periods, followed by a short string.
        - "network_interfaces" is a list of the MAC addresses of any network interfaces available to the system. Each element in this list should be a string containing a hexadecimal MAC address.
    - "processing" is a dictionary that contains diagnostic information regarding the processing of images.
        - "captured_timestamp" is a decimal number indicating when the image capture completed, as a Unix timestamp. This should always be a positive decimal number.
        - "processing_time" is a decimal number indicating how long the ALPR processing sequence took, in seconds. This should always be a positive decimal number.
        - "processed_timestamp" is a decimal number indicating when the ALPR processing sequence completed, as a Unix timestamp. This should always be a positive decimal number.
    - "image" is a dictionary that contains diagnostic information regarding the capturing of images.
        - "width" is an integer number indicating the width of the captured image, after processing, in pixels. This should always be a positive integer number.
        - "height" is an integer number indicating the height of the image captured, after processing, in pixel. This should always be a positive integer number.
- "results" is a list containing the license plate analysis results themselves. 
    - Each entry inside this list is a list in itself, with each parent list representing a detected license plate. The child list associated with each license plate contains several dictionaries of the most-likely guesses as to the contents of the license plate.
        - "plate" is a string containing the text for the guess. This value should only contain alphanumeric characters.
        - "confidence" is the confidence percentage for the guess. This value will always be within the range of 0 to 100, and can be fractional.

### Example

Below is an example of results received from Predator Fabric.

```json
{
	"info": {
		"identifier": "abcdef123456789",
		"timezone": ["EST", "EDT"],
        "system": {
            "python_version": "3.10.6 final",
            "network_interfaces": ["2C:F0:5B:74:AC:8C", "2C:F0:5B:DD:9B:55"]
        }
		"processing": {
			"captured_timestamp": 1675851928.664179,
			"processing_time": 0.2290651,
			"processed_timestamp": 1675851929.181615
		},
		"image": {
			"width": 4096,
			"height": 2304
		}
	},
	"results": [
		[
            {
                "plate": "ARIZONA",
                "confidence": 89.265213
            }, {
                "plate": "ARIZ0NA",
                "confidence": 87.295868
            }, {
                "plate": "ARIZQNA",
                "confidence": 82.179695
            }, {
                "plate": "ARIZON",
                "confidence": 81.358353
            }
        ],
      	[
          	{
                "plate": "ISO8152",
                "confidence": 93.559486
            }, {
                "plate": "IS08152",
                "confidence": 86.41243
            }, {
                "plate": "IS08I52",
                "confidence": 83.381683
            }, {
                "plate": "IS086D1",
                "confidence": 82.626686
            }
        ],
        [
            {
                "plate": "522UXS",
                "confidence": 87.155853
		    }
        ]
	]
}

```


## Networking

First and foremost, the Predator Fabric instance needs to be configured to send data to the remote service. This can be done under the 'networking' section of the configuration. To learn more see the [CONFIGURATION.md](CONFIGURATION.md) document.

On a basic level, Predator Fabric submits a string of JSON data to the remote service in a POST request. To receive and handle this data, load the "results" key from the POST data as a JSON string.

### Basics

Below is a bare-bones example of accepting data from Predator Fabric using PHP. Note that this example will fail if the information received is not valid JSON. It is highly recommended to add basic JSON validation at this step in a production environment.

```PHP
$received_data = strval($_POST["results"]); // Get the raw submitted results.
$processed_data = json_decode($received_data); // Decode the JSON data received.
```

### Authentication

In order to verify that this information was sent from a known device, you should authenticate it using it's identifier. For example, your service might have a database of users, each with a list of registered keys. In this case, you might look to find a match for the identifier in the user database keys. This step also helps filter out submissions from unknown users. Below is a basic example of authentication wrriten in PHP.

```PHP
$identifier = strval($processed_data["identifier"]); // Get the identifier from the data submission as a string.

$identifier = filter_var($identifier, FILTER_SANITIZE_STRING); // Sanitize the identifier string.

if (strlen($identifier) != 32) { exit(); } // Verify that the identifier is the expected length. Otherwise, terminate the script.

$associated_user = "";
foreach ($user_database as $username => $keys) { // Iterate through all users.
    if (in_array($identifier, $keys) == true) { // Check to see the identifier matches any of this user's keys
        $associated_user = $username;
    }
}

if ($associated_user != "") { // Check to see if an associated user was found.
    // The key was authenticated as being owned by $associated_user.
    // Processing can continue.
}
```

### Validation

After authentication, it's worth verifying that the information received matches the expected structure, as described above. For ideal security and stability, you should verify that each piece of data your service handles is within expected parameters before using or saving it.

Expected criteria for each value is described in the "Structure Overview" section above.
