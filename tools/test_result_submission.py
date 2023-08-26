# This script submits example results to a target, just as Predator Fabric would.
# This can be used to make sure your target is properly setup to receive results without needing to run the full program.
import requests
import time


submission_target = "http://localhost/premonition/ingest.php"
submission_data = '{"info":{"identifier":"abcdef123456789","timezone":["EST","EDT"],"system":{"python_version":"3.10.6 final","network_interfaces":["2C:F0:5B:74:AC:8C","2C:F0:5B:DD:9B:55"]},"processing":{"captured_timestamp":' + str(time.time()) + ',"processing_time":0.2290651,"processed_timestamp":' + str(time.time() + 0.2290651) + '},"image":{"width":4096,"height":2304}},"results":[[{"plate":"ARIZONA","confidence":89.265213},{"plate":"ARIZ0NA","confidence":87.295868},{"plate":"ARIZQNA","confidence":82.179695},{"plate":"ARIZON","confidence":81.358353}],[{"plate":"ISO8152","confidence":93.559486},{"plate":"IS08152","confidence":86.41243},{"plate":"IS08I52","confidence":83.381683},{"plate":"IS086D1","confidence":82.626686}],[{"plate":"522UXS","confidence":87.155853}]]}'




print("Submitting data:")
print(submission_data)

print("\n\n")


request = requests.post(submission_target, data={"results": submission_data}, timeout=5) # Submit the JSON string of the results to the specified target.

print("Response:")
print (request.text)
