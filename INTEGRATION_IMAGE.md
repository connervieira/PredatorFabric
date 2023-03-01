# Results Receiving

This document explains how to integrate Predator Fabric with a receiver system.

These instructions explain the process of handling images sent by Predator Fabric. For information regarding result receiving, see the [INTEGRATION_RESULTS.md](INTEGRATION_RESULTS.md) document.


## Structure

### Overview

The data sent by Predator Fabric to the remote service regarding images follows this structure.

- "image" contains the image data, encoded as Base64.
- "identifier" is a string that contains an identifier set in the Predator Fabric configuration. This value is intended to be used like an API key, and to be used to authenticate a particular device before handling data received from it.


### Example

Below is an example of image data received from Predator Fabric. The Base64 data has been abbreviated for sake of readability.

```json
{
	"image": "ZBEauVODlggVW+YaMlAbQhQqU9cY2qo..."
    "identifier": "abcdef123456789"
}

```


## Networking

The Predator Fabric instance needs to be configured to send image data to a remote service. This can be done under the 'networking' section of the configuration. To learn more see the [CONFIGURATION.md](CONFIGURATION.md) document.

On a basic level, Predator Fabric submits a string of JSON data to the remote service in a POST request. To receive and handle this data, load the "image" key from the POST data as a JSON string.

### Basics

Below is a bare-bones example of accepting image data from Predator Fabric using PHP. Note that this example will fail if the information received is not valid JSON. It is highly recommended to add basic JSON validation at this step in a production environment.

```PHP
$received_data = strval($_POST["image"]); // Get the submitted image data.
$processed_data = json_decode($received_data, true); // Decode the JSON data received.

$image_data = base64_decode($processed_data["image"]); // Decode the image from the received data.
```

### Authentication

Before the received image is saved or otherwise processed, the source should be authenticated.

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
