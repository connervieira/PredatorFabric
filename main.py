# Copyright (C) 2023 V0LT - Conner Vieira 

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.


print("Loading...")


import os # Required to interact with certain operating system functions.
import sys # Required to interact with certain operating system functions.
import json # Required to process JSON data.


root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the path of the root directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.


config = json.load(open(root_directory + "/config.json")) # Load the configuration database from config.json

import utils # Import the utils.py scripts.
debug_message = utils.debug_message # Load the debug message function from the utils script.
error = utils.error # Load the error message function from the utils script.
heartbeat = utils.heartbeat # Load the heartbeat message function from the utils script.
log_plates = utils.log_plates # Load the plate logging function from the utils script.
style = utils.style # Load the style from the utils script.
clear = utils.clear # Load the screen clearing function from the utils script.
submit_results = utils.submit_results # Load the result submission function from the utils script.
verify_configuration = utils.verify_configuration # Load the configuration validation function from the utils script.


debug_message("Importing 'time' library")
import time # Required to add delays and handle dates/times.
debug_message("Importing 'datetime' library")
import datetime # Required for converting between timestamps and human readable date/time information.
debug_message("Importing 'requests' library")
import requests # Required for making network requests.
debug_message("Importing 'psutil' library")
import psutil # Required to get information regarding network interfaces.
debug_message("Importing 're' library")
import re # Required to handle regular expressions.
import base64 # Required to encode images.


import ignore # Import the library to handle license plates in the ignore list.
ignore_list = ignore.fetch_ignore_list() # Fetch the ignore lists.




# Verify the integrity of the configuration.
invalid_configuration_options = verify_configuration(config) # Run validation on the configuration.
if (len(invalid_configuration_options) > 0): # Check to see if there were any invalid configuration options detected by the validation process.
    if (len(invalid_configuration_options) > 1): # Check to see if there are multiple invalid configuration options.
        error("Invalid configuration options: " + str(invalid_configuration_options))
    elif (len(invalid_configuration_options) == 1): # Check to see if there is a single invalid configuration option.
        error("Invalid configuration option: " + str(invalid_configuration_options))



debug_message("Completed start-up process")


# Display the start-up intro header.
clear() # Clear the console output.
debug_message("Displaying start-up header")
print(style.bold + config["general"]["name"] + style.end)
if (config["general"]["start_message"] != ""): # Only display the line for the custom message if the user has defined one.
    print(config["general"]["start_message"]) # Show the user's custom defined start-up message.





debug_message("Getting network interfaces")
network_interfaces = [] # Set this list of network interface MAC addresses to a blank placeholder list.
for interface in psutil.net_if_addrs(): # Iterate through each network interface.
    if (psutil.net_if_addrs()[interface][0].address): # Check to see if this interface has an address.
        interface_address = psutil.net_if_addrs()[interface][0].address # Get the address of this interface.
        if (re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", interface_address.lower())): # Check to see if this address is a MAC address.
            network_interfaces.append(interface_address) # Add this MAC address to the list of interfaces.



debug_message("Starting main loop")
while True: # Run in a loop forever, until terminated.


    clear() # Clear the console output.

    debug_message("Delaying based on interval")
    time.sleep(int(config["general"]["interval"]))




    # ===== Capture an image =====
    debug_message("Capturing image")
    if (config["image"]["camera"]["provider"].lower() == "fswebcam"): # Check to see if the configured camera backend is FSWebcam.
        os.system("fswebcam --no-banner -r " + config["image"]["camera"]["resolution"] + " -d " + config["image"]["camera"]["device"] + " --jpeg 100 " + config["image"]["camera"]["arguments"] + " " + config["developer"]["working_directory"] + "/" + config["image"]["camera"]["file_name"] + " >/dev/null 2>&1") # Take a photo using FSWebcam, and save it to the working directory.
    elif (config["image"]["camera"]["provider"].lower() == "imagesnap"): # Check to see if the configured camera backend is ImageSnap.
        os.system("imagesnap -q -d " + config["image"]["camera"]["device"] + " " + config["image"]["camera"]["arguments"] + " " + config["developer"]["working_directory"] + "/" + config["image"]["camera"]["file_name"]) # Take a photo using ImageSnap, and save it to the working directory.
    elif (config["image"]["camera"]["provider"] == "off"): # Check to see if the camera backend is disabled.
        pass # Image capture is disabled, so do nothing.
    else:
        error("Unrecognized camera provider.")

    image_captured_time = time.time() # Record the time that the image was captured.







    image_file = config["developer"]["working_directory"] + "/" + config["image"]["camera"]["file_name"] # Get the absolute path to the image file.
    if (os.path.exists(image_file) == True): # Check to make sure the captured image file actually exists before processing it.


        # ===== Process the image =====
        debug_message("Processing image")

        # If necessary, rotate the image.
        if (config["image"]["processing"]["rotation"]["enabled"] == True): # Check to see if image rotation is enabled.
            debug_message("Rotating image")
            os.system("convert " + image_file + " -rotate " + str(config["image"]["processing"]["rotation"]["angle"]) + " " + image_file) # Execute the command to rotate the image, based on the configuration.


        # If enabled, crop the image.
        if (config["image"]["processing"]["cropping"]["enabled"] == True): # Check to see if image cropping is enabled.
            debug_message("Cropping image")
            os.system(root_directory + "/crop " + image_file + " " + str(config["image"]["processing"]["cropping"]["left_margin"]) + " " + str(config["image"]["processing"]["cropping"]["right_margin"]) + " " + str(config["image"]["processing"]["cropping"]["top_margin"]) + " " + str(config["image"]["processing"]["cropping"]["bottom_margin"])) # Execute the command to crop the image.





        # ===== Run ALPR on the captured image ====
        debug_message("Running ALPR")

        if (config["alpr"]["engine"] == "openalpr"): # The configured ALPR engine is OpenALPR.
            analysis_command = "alpr -j -n " + str(config["alpr"]["guesses"]) + " '" + image_file + "'" # Prepare the analysis command so it can be run in the next step.

            raw_reading_output = str(os.popen(analysis_command).read()) # Run the OpenALPR command, and save it's raw output.

            try: # Run the JSON interpret command inside a 'try' block, so the entire program doesn't fatally crash if the JSON data is malformed.
                alpr_output = json.loads(raw_reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
            except: # If the ALPR output fails to be parsed, then do the following.
                alpr_output = json.loads('{"version":0,"data_type":"alpr_results","epoch_time":0,"img_width":0,"img_height":0,"processing_time_ms":0,"regions_of_interest":[{"x":0,"y":0,"width":0,"height":0}],"results":[]}') # Use a blank placeholder for the ALPR reading output, since the actual reading output was malformed.


        elif (config["alpr"]["engine"] == "phantom"): # The configured ALPR engine is Phantom.
            analysis_command = "alpr -n " + str(config["alpr"]["guesses"]) + " '" + image_file + "'" # Prepare the analysis command so it can be run in the next step.
            raw_reading_output = str(os.popen(analysis_command).read()) # Run the Phantom ALPR command, and save it's raw output.

            try: # Run the JSON interpret command inside a 'try' block, so the entire program doesn't fatally crash if the JSON data is malformed.
                alpr_output = json.loads(raw_reading_output) # Convert the JSON string from the command output to actual JSON data that Python can manipulate.
            except: # If the ALPR output fails to be parsed, then do the following.
                alpr_output = json.loads('{"version":0,"data_type":"alpr_results","epoch_time":0,"img_width":0,"img_height":0,"processing_time_ms":0,"regions_of_interest":[{"x":0,"y":0,"width":0,"height":0}],"results":[]}') # Use a blank placeholder for the ALPR reading output, since the actual reading output was malformed.



        else: # The configured ALPR engine is not recognized.
            alpr_output = json.loads('{"version":0,"data_type":"alpr_results","epoch_time":0,"img_width":0,"img_height":0,"processing_time_ms":0,"regions_of_interest":[{"x":0,"y":0,"width":0,"height":0}],"results":[]}') # Use a blank placeholder for the ALPR reading output, since there was a problem running ALPR analysis.
            error("The configured ALPR engine is not recognized.")


        if (config["developer"]["print_alpr_diagnostics"] == True):
            print("Detected " + str(len(alpr_output["results"])) + " plates")
            print(alpr_output)
            if (len(alpr_output["results"]) > 0):
                for plate in alpr_output["results"]:
                    print(plate["plate"])








    else: # If the captured image file does not exist, then display an error, and use placeholder data.
        alpr_output = json.loads('{"version":0,"data_type":"alpr_results","epoch_time":0,"img_width":0,"img_height":0,"processing_time_ms":0,"regions_of_interest":[{"x":0,"y":0,"width":0,"height":0}],"results":[]}') # Use a blank placeholder for the ALPR reading output, since there was a problem running ALPR analysis.
        error("The captured image file does not exist. There may be a problem with the camera.")








    # ===== Process ALPR results =====
    debug_message("Processing ALPR results")

    alpr_processed_time = time.time()

    alpr_results = {
    "info": {
        "identifier": config["network"]["identifier"],
        "timezone": time.tzname,
        "system": {
            "python_version": str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + " " + str(sys.version_info[3]),
            "network_interfaces": network_interfaces
        },
        "processing": {
            "captured_timestamp": image_captured_time,
            "processing_time": alpr_output["processing_time_ms"]/1000,
            "processed_timestamp": alpr_processed_time 
        },
        "image": {
            "width": alpr_output["img_width"],
            "height": alpr_output["img_height"]
        }
    },
        "results": []
    }

    for plate in alpr_output["results"]: # Iterate through each plate detected in the raw output.
        guesses = [] # Set the list of guesses for this plate to a blank placeholder.
        ignore_current_plate = False # Reset this variable to 'false' for each detected plate.
        for guess in plate["candidates"]: # Iterate through each guess for each plate.
            if (guess["plate"].upper() in ignore_list): # Check to see if this guess is in the list of plates to ignore.
                ignore_current_plate = True # Indicate that this plate should be ignored.
            if (int(guess["confidence"]) >= int(config["alpr"]["confidence"])): # Verify that the confidence level for this guess is above the minimum confidence threshold.
                guesses.append({"plate": guess["plate"], "confidence": guess["confidence"]}) # Add the information for this guess to the list of guesses for this plate.
            
        if (ignore_current_plate == False): # Only add this plate to the list of results if it is not marked as a plate to be ignored.
            alpr_results["results"].append(guesses) # Add the guesses for this plate to the complete list of ALPR results.





    # ===== Submit detected license plates to a network service =====
    if (len(alpr_results["results"]) > 0): # Only submit results if there were license plates detected.
        debug_message("Submitting ALPR results")
        if (config["network"]["results_submission"]["mode"] == "on" or (config["network"]["results_submission"]["mode"] == "auto" and len(alpr_results["results"]) > 0)): # Check to see if remote image processing is enabled.
            submit_results(alpr_results, config["network"]["results_submission"]["target"]) # Execute the function to submit data to the configured target.





    # ===== Upload captured image to external service, if necessary =====
    if (config["network"]["remote_processing"]["mode"] == "on" or (config["network"]["remote_processing"]["mode"] == "auto" and len(alpr_results["results"]) > 0)): # Check to see if remote image processing is enabled.
        debug_message("Uploading image data")
        if (os.path.exists(image_file) == True): # Check to make sure the captured image file actually exists before attempting to upload it.
            with open(image_file, 'rb') as image_file: # Open the image file.
                encoded_image_file = str(base64.b64encode(image_file.read())) # Read the image file, encoded as base 64, and convert it to a string.

            if (encoded_image_file[0:2] == "b'"): # Check to see if the string has characters indicating that it is a bytes literal.
                encoded_image_file = encoded_image_file[2:-1] # Remove the first two characters and last single character, since they only serve to indicate that the string is a bytes literal.

            image_submission_information = {"image": encoded_image_file, "identifier": config["network"]["identifier"] } # Prepare the image information bundle.
            raw_image_submission_information = json.dumps(image_submission_information) # Convert the image information bundle into a string.

            request = requests.post(config["network"]["remote_processing"]["target"], data={"image": raw_image_submission_information}, timeout=20) # Submit the JSON string of the image information to the specified target.

        else:
            error("The captured image could not be uploaded, since the file does not exist.")









    # ===== Update interface directory files =====
    debug_message("Sending UI heartbeat")
    heartbeat()
    log_plates(alpr_results)
