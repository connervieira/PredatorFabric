# Copyright (C) 2023 V0LT - Conner Vieira

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program (LICENSE)
# If not, see https://www.gnu.org/licenses/ to read the license agreement.





# This script contains several funtions and classes used in main.py





import os # Required to interact with certain operating system functions.
import json # Required to process JSON data.
import time # Required to manage delays.
import re # Required to use regex.
import validators # Required to validate URLs.
import requests # Required top make network requests.

root_directory = str(os.path.dirname(os.path.realpath(__file__))) # This variable determines the folder path of the root Predator directory. This should usually automatically recognize itself, but it if it doesn't, you can change it manually.

config = json.load(open(root_directory + "/config.json")) # Load the configuration database from config.json






# Define some styling information.
class style:
    # Define colors
    purple = '\033[95m'
    cyan = '\033[96m'
    blue = '\033[94m'
    green = '\033[92m'
    yellow = '\033[93m'
    gray = '\033[1;37m'
    red = '\033[91m'

    # Define text decoration
    bold = '\033[1m'
    underline = '\033[4m'
    italic = '\033[3m'
    faint = '\033[2m'

    # Define styling end marker
    end = '\033[0m'


# Define the function to print debugging information when the configuration specifies to do so.
debugging_time_record = {}
debugging_time_record["Main"] = time.time() # This value holds the time that the previous debug message in the main thread was displayed.
debugging_time_record["ALPRStreamMaintainer"] = time.time() # This value holds the time that the previous debug message in the ALPR stream maintainer thread was displayed.
debugging_time_record["ALPRStream"] = time.time() # This value holds the time that the previous debug message in the ALPR stream thread was displayed.
for device in config["image"]["camera"]["device"]: # Iterate over each device in the configuration.
    debugging_time_record["ALPRStream" + str(device)] = time.time() # Initialize each debug timer.
def debug_message(message, thread="Main"):
    if (config["developer"]["debug_mode"] == True): # Only print the message if the debugging output configuration value is set to true.
        global debugging_time_record
        time_since_last_message = (time.time()-debugging_time_record[thread]) # Calculate the time since the last debug message.
        print(f"{style.italic}{style.faint}{time.time():.10f} ({time_since_last_message:.10f} - {thread}) - {message}{style.end}") # Print the message.
        debugging_time_record[thread] = time.time() # Record the current timestamp.




# Define the function that will be used to save text to files.
def save_to_file(file_name, contents, silence=False):
    file = None
    success = False
    try:
        file = open(file_name, 'w')
        file.write(contents)
        success = True   
        if (silence == False):
            print("Successfully saved at " + file_name + ".")
    except IOError as error_message:
        success = False
        if (silence == False):
            print(error_message)
            print("Failed to save!")
    finally:
        try:
            if file:
                file.close()
        except:
            success = False
    return success





def is_json(string):
    try:
        json_object = json.loads(string) # Try to load string as JSON information.
    except ValueError as error_message: # If the process fails, then the string is not valid JSON.
        return False # Return 'false' to indicate that the string is not JSON.

    return True # If the try statement is successful, then return 'true' to indicate that the string is valid JSON.




# Define the function used to handle error messages.
error_file_location = config["developer"]["interface_directory"] + "/errors.json"
if (os.path.exists(error_file_location) == False): # If the error log file doesn't exist, create it.
    save_to_file(error_file_location, "{}", True) # Save a blank placeholder dictionary to the error log file.

error_file = open(error_file_location, "r") # Open the error log file for reading.
error_file_contents = error_file.read() # Read the raw contents of the error file as a string.
error_file.close() # Close the error log file.

if (is_json(error_file_contents) == True): # If the error file contains valid JSON data, then load it.
    error_log = json.loads(error_file_contents) # Read and load the error log from the file.
else: # If the error file doesn't contain valid JSON data, then load a blank placeholder in it's place.
    error_log = json.loads("{}") # Load a blank placeholder dictionary.

def error(message):
    print(style.red + str(message) + style.end)
    error_log[time.time()] = message # Add this error message to the log file, using the current time as the key.
    save_to_file(error_file_location, json.dumps(error_log), True) # Save the modified error log to the disk as JSON data.





# Define the function used to handle system heartbeats, which allow external services to verify that the program is running.
heartbeat_file_location = config["developer"]["interface_directory"] + "/heartbeat.json"
if (os.path.exists(heartbeat_file_location) == False): # If the heartbeat log file doesn't exist, create it.
    save_to_file(heartbeat_file_location, "[]", True) # Save a blank placeholder list to the heartbeat log file.

heartbeat_file = open(heartbeat_file_location, "r") # Open the heartbeat log file for reading.
heartbeat_file_contents = heartbeat_file.read() # Read the raw contents of the heartbeat file as a string.
heartbeat_file.close() # Close the heartbeat log file.

if (is_json(heartbeat_file_contents) == True): # If the heartbeat file contains valid JSON data, then load it.
    heartbeat_log = json.loads(heartbeat_file_contents) # Read and load the heartbeat log from the file.
else: # If the heartbeat file doesn't contain valid JSON data, then load a blank placeholder in it's place.
    heartbeat_log = json.loads("[]") # Load a blank placeholder list.


def heartbeat():
    global heartbeat_log
    print("Running... (" + str(round(time.time())) + ")") # Print a message to the console with the current time..
    heartbeat_log.append(time.time()) # Add this pulse to the heartbeat log file, using the current time as the key.
    heartbeat_log = heartbeat_log[-int(config["developer"]["max_heartbeat_history"]):] # Trim the list to only contain the last entries.
    save_to_file(heartbeat_file_location, json.dumps(heartbeat_log), True) # Save the modified heartbeat log to the disk as JSON data.





# Define the function used to handle the license plate reading history, which allow external services to see license plate recognition data for diagnostic purposes.
plate_file_location = config["developer"]["interface_directory"] + "/plates.json"
if (os.path.exists(plate_file_location) == False): # If the plate log file doesn't exist, create it.
    save_to_file(plate_file_location, "{}", True) # Save a blank placeholder dictionary to the plate log file.

plate_file = open(plate_file_location, "r") # Open the plate log file for reading.
plate_file_contents = plate_file.read() # Read the raw contents of the plate file as a string.
plate_file.close() # Close the plate log file.

if (is_json(plate_file_contents) == True): # If the plate file contains valid JSON data, then load it.
    plate_log = json.loads(plate_file_contents) # Read and load the plate log from the file.
else: # If the plate log file doesn't contain valid JSON data, then load a blank placeholder in it's place.
    plate_log = json.loads("{}") # Load a blank placeholder dictionary.


def log_plates(alpr_output):
    global plate_log


    detected_plates = {} # Set the collection of detected plates to a blank dictionary.
    for plate in alpr_output["results"]: # Iterate through all of the detect plates in the ALPR results.
        if (len(plate) > 0):
            detected_plates[plate[0]["plate"]] = {} # Define this plate by its most likely guess.
            for guess in plate: # Iterate through all of the guesses for each detected plate in the ALPR results.
                detected_plates[plate[0]["plate"]][guess["plate"]] = guess["confidence"] # Add each guess to this plate, along with it's confidence level.
        
    plate_log[time.time()] = detected_plates


    entries_to_remove = [] # Create a blank placeholder list to hold all of the entry keys that have expired and need to be removed.

    for entry in plate_log.keys(): # Iterate through each entry in the plate history.
        if (time.time() - float(entry) > config["developer"]["max_plate_history_age"]): # Check to see if this entry has expired according the max age configuration value.
            entries_to_remove.append(entry) # Add this entry key to the list of entries to remove.

    for key in entries_to_remove: # Iterate through each of the keys designated to be removed.
        plate_log.pop(key)

    save_to_file(plate_file_location, json.dumps(plate_log), True) # Save the modified plate log to the disk as JSON data.





# Define the function that will be used to clear the screen.
def clear():
    if (config["developer"]["debug_mode"] == False): # Only clear the screen if debugging mode is disabled.
        os.system("clear") # Execute the command to clear the console on Unix based systems.






def submit_results(results, target):
    debug_message("Uploading ALPR results")
    if (validators.url(target)): # Verify that the target host is a valid URL.
        raw_results_string = json.dumps(results) # Convert the results to a JSON string.
        request = requests.post(target, data={"results": raw_results_string}, timeout=5) # Submit the JSON string of the results to the specified target.





# Define the function that will be used to verify the integrity of the configuration.
def verify_configuration(config):
    debug_message("Validating configuration")
    invalid_values = [] # This is a placeholder list that will hold all of the invalid options.

    if ("general" in config): # Verify that the 'general' configuration section exists.
        if (type(config["general"]["name"]) != str): # Verify the variable type of the 'name' configuration value.
            invalid_values.append("config>general>name") # Add the 'name' value to the list of invalid options.
        if (type(config["general"]["start_message"]) != str): # Verify the variable type of the 'name' configuration value.
            invalid_values.append("config>general>start_message") # Add the 'start_message' value to the list of invalid options.
        if (type(config["general"]["interval"]) != int): # Verify the variable type of the 'interval' configuration value.
            invalid_values.append("config>general>interval") # Add the 'interval' value to the list of invalid options.
        if (config["general"]["mode"] not in ["discrete", "stream"]):
            invalid_values.append("config>general>mode")
    else:
        invalid_values.append("config>general") # Add the 'general' section to the list of invalid options.


    if ("image" in config): # Verify that the 'image' configuration section exists.
        if ("camera" in config["image"]): # Verify that the 'processing' configuration section exists.
            if (config["image"]["camera"]["provider"] != "fswebcam" and config["image"]["camera"]["provider"] != "imagesnap" and config["image"]["camera"]["provider"] != "off"): # Verify the that the 'provider' value matches a valid option.
                invalid_values.append("config>image>provider") # Add the 'provider' value to the list of invalid options.
            if (type(config["image"]["camera"]["device"]) != list): # Verify the variable type of the 'camera_device' configuration value.
                invalid_values.append("config>image>camera>device") # Add the 'device' value to the list of invalid options.
            if (re.fullmatch("(\d\d\dx\d\d\d)", config["image"]["camera"]["resolution"]) == None and re.fullmatch("(\d\d\d\dx\d\d\d)", config["image"]["camera"]["resolution"]) == None and re.fullmatch("(\d\d\d\dx\d\d\d\d)", config["image"]["camera"]["resolution"]) == None): # Verify that the 'resolution' setting matches the format 000x000, 0000x000, or 0000x0000.
                invalid_values.append("config>image>camera>resolution")
            if (type(config["image"]["camera"]["arguments"]) != str): # Verify the variable type of the 'arguments' configuration value.
                invalid_values.append("config>image>camera>arguments") # Add the 'arguments' value to the list of invalid options.
            if (type(config["image"]["camera"]["file_name"]) != str or config["image"]["camera"]["file_name"] == ""): # Verify the variable type of the 'file_name' configuration value, and that the value isn't blank.
                invalid_values.append("config>image>camera>file_name") # Add the 'file_name' value to the list of invalid options.
        else:
            invalid_values.append("config>image>camera") # Add the 'camera' section to the list of invalid options.
        if ("processing" in config["image"]): # Verify that the 'processing' configuration section exists.
            if ("cropping" in config["image"]["processing"]): # Verify that the 'cropping' configuration section exists.
                if (type(config["image"]["processing"]["cropping"]["enabled"]) != bool): # Verify the variable type of the 'enabled' configuration value.
                    invalid_values.append("config>image>processing>cropping>enabled") # Add the 'enabled' value to the list of invalid options.
                if (type(config["image"]["processing"]["cropping"]["left_margin"]) != int): # Verify the variable type of the 'left_margin' configuration value.
                    invalid_values.append("config>image>processing>cropping>left_margin") # Add the 'left_margin' value to the list of invalid options.
                if (type(config["image"]["processing"]["cropping"]["right_margin"]) != int): # Verify the variable type of the 'right_margin' configuration value.
                    invalid_values.append("config>image>processing>cropping>right_margin") # Add the 'right_margin' value to the list of invalid options.
                if (type(config["image"]["processing"]["cropping"]["top_margin"]) != int): # Verify the variable type of the 'top_margin' configuration value.
                    invalid_values.append("config>image>processing>cropping>top_margin") # Add the 'top_margin' value to the list of invalid options.
                if (type(config["image"]["processing"]["cropping"]["bottom_margin"]) != int): # Verify the variable type of the 'bottom_margin' configuration value.
                    invalid_values.append("config>image>processing>cropping>bottom_margin") # Add the 'bottom_margin' value to the list of invalid options.
            else:
                invalid_values.append("config>image>processing>cropping") # Add the 'cropping' section to the list of invalid options.

            if ("rotation" in config["image"]["processing"]): # Verify that the 'rotation' configuration section exists.
                if (type(config["image"]["processing"]["rotation"]["enabled"]) != bool): # Verify the variable type of the 'enabled' configuration value.
                    invalid_values.append("config>image>processing>rotation>enabled") # Add the 'enabled' value to the list of invalid options.
                if (type(config["image"]["processing"]["rotation"]["angle"]) != int): # Verify the variable type of the 'angle' configuration value.
                    invalid_values.append("config>image>processing>rotation>angle") # Add the 'angle' value to the list of invalid options.
            else:
                invalid_values.append("config>image>processing>rotation") # Add the 'rotation' section to the list of invalid options.
        else:
            invalid_values.append("config>image>processing") # Add the 'processing' section to the list of invalid options.
    else:
        invalid_values.append("config>image") # Add the 'image' section to the list of invalid options.


    if ("alpr" in config): # Verify that the 'alpr' configuration section exists.
        if (config["alpr"]["engine"] != "openalpr" and config["alpr"]["engine"] != "phantom"): # Verify the that the 'engine' value matches a valid option.
            invalid_values.append("config>alpr>engine") # Add the 'engine' section to the list of invalid options.
        if (type(config["alpr"]["guesses"]) != int or config["alpr"]["guesses"] <= 0): # Verify the variable type of the 'guesses' configuration value, and that the value is greater than 0.
            invalid_values.append("config>alpr>guesses") # Add the 'guesses' section to the list of invalid options.
        if (type(config["alpr"]["confidence"]) != int or config["alpr"]["confidence"] < 0 or config["alpr"]["confidence"] > 100): # Verify the variable type of the 'confidence' configuration value, and that the value is within expected limits.
            invalid_values.append("config>alpr>confidence") # Add the 'confidence' section to the list of invalid options.
    else:
        invalid_values.append("config>alpr") # Add the 'alpr' section to the list of invalid options.


    if ("network" in config): # Verify that the 'network' configuration section exists.
        if (type(config["network"]["identifier"]) != str): # Verify the variable type of the 'identifier' configuration value.
            invalid_values.append("config>network>identifier") # Add the 'identifier' value to the list of invalid options.

        if ("results_submission" in config["network"]): # Verify that the 'results_submission' configuration section exists.
            if (not validators.url(config["network"]["results_submission"]["target"])): # Verify that the 'target' value is a valid URL.
                invalid_values.append("config>network>results_submission>target") # Add the 'target' value to the list of invalid options.
        else:
            invalid_values.append("config>network>results_submission") # Add the 'results_submission' section to the list of invalid options.

        if ("remote_processing" in config["network"]): # Verify that the 'remote_processing' configuration section exists.
            if (not validators.url(config["network"]["remote_processing"]["target"])): # Verify that the 'target' value is a valid URL.
                invalid_values.append("config>network>remote_processing>target") # Add the 'target' value to the list of invalid options.
            if (config["network"]["remote_processing"]["mode"] != "off" and config["network"]["remote_processing"]["mode"] != "auto" and config["network"]["remote_processing"]["mode"] != "on"): # Verify that the 'mode' value matches an expected option.
                invalid_values.append("config>network>remote_processing>mode") # Add the 'mode' value to the list of invalid options.
        else:
            invalid_values.append("config>network>remote_processing") # Add the 'remote_processing' section to the list of invalid options.
    else:
        invalid_values.append("config>network") # Add the 'network' section to the list of invalid options.



    if ("developer" in config): # Verify that the 'developer' configuration section exists.
        if (type(config["developer"]["debug_mode"]) != bool): # Verify the variable type of the 'debug_mode' configuration value.
            invalid_values.append("config>developer>debug_mode") # Add the 'debug_mode' section to the list of invalid options.
        if (os.path.isdir(config["developer"]["working_directory"]) == False): # Verify that the 'working_directory' option points to a valid directory.
            invalid_values.append("config>developer>working_directory") # Add the 'working_directory' value to the list of invalid options.
        if (os.path.isdir(config["developer"]["interface_directory"]) == False): # Verify that the 'interface_directory' option points to a valid directory.
            invalid_values.append("config>developer>interface_directory") # Add the 'interface_directory' value to the list of invalid options.
        if (type(config["developer"]["print_alpr_diagnostics"]) != bool): # Verify the variable type of the 'print_alpr_diagnostics' configuration value.
            invalid_values.append("config>developer>print_alpr_diagnostics") # Add the 'print_alpr_diagnostics' value to the list of invalid options.
        if (type(config["developer"]["max_heartbeat_history"]) != int): # Verify the variable type of the 'max_heartbeat_history' configuration value.
            invalid_values.append("config>developer>max_heartbeat_history") # Add the 'max_heartbeat_history' value to the list of invalid options.
        if (type(config["developer"]["max_plate_history_age"]) != int): # Verify the variable type of the 'max_plate_history_age' configuration value.
            invalid_values.append("config>developer>max_plate_history_age") # Add the 'max_plate_history_age' value to the list of invalid options.
        if ("ignore_list" in config["developer"]): # Verify that the 'ignore_list' configuration section exists.
            if (type(config["developer"]["ignore_list"]["enabled"]) != bool): # Verify the variable type of the 'enabled' configuration value.
                invalid_values.append("config>network>ignore_list>enabled") # Add the 'enabled' section to the list of invalid options.
            if (os.path.exists(config["developer"]["working_directory"] + "/" + config["developer"]["ignore_list"]["local_file"]) == False): # Verify that the 'local_file' value points to a valid file.
                invalid_values.append("config>developer>ignore_list>local_file") # Add the 'local_file' value to the list of invalid options.
            if (type(config["developer"]["ignore_list"]["remote_sources"]) != list): # Verify the variable type of the 'remote_sources' configuration value.
                invalid_values.append("config>network>ignore_list>remote_sources") # Add the 'remote_sources' section to the list of invalid options.
    else:
        invalid_values.append("config>developer") # Add the 'network' section to the list of invalid options.


        

    return invalid_values
