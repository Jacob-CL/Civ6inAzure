import tailer
import re
import threading
import csv
import time
import logging
import traceback
import json
import os
from azure.identity import DefaultAzureCredential
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.core.exceptions import HttpResponseError

# logging.basicConfig(level=logging.DEBUG, format='---> %(levelname)s - %(message)s')
# logging.info("LogSender.py started...")

files = [ 
    {'type': 'log', 'path': 'C:\\Users\\User\\AppData\\Local\\Firaxis Games\\Sid Meier\'s Civilization VI\\Logs\\AStar_GC.log'},
]

############################################################################################################################
############################################################################################################################

def monitor_log_file(log_file_path):
    while True:
        try:        
            with open(log_file_path, "r") as logfile:
                if log_file_path == "C:\\Users\\User\\AppData\\Local\\Firaxis Games\\Sid Meier\'s Civilization VI\\Logs\\AStar_GC.log":
                    print('Found log file..')
                    AStarGC_json = convert_logfile_data_to_json(log_file_path)
                    send_it("Custom-AStarGC_CL", AStarGC_json)
                    print("Sent log file!")
                    print("Now listening for new lines...")

                    # Now continue to monitor for new lines
                    for line in tailer.follow(logfile):
                        print("I found a new line!")
                        line_json = convert_new_logline_to_json(log_file_path, line)
                        send_it("Custom-AStarGC_CL", line_json)
                        print("New lines sent!")                 

        except HttpResponseError or FileNotFoundError as e:
                if FileNotFoundError:
                    print(f"File {log_file_path} not found, checking again in 1 seconds.")
                    time.sleep(1)  # Wait for some time before checking again, e.g., 10 seconds
                else:
                    print(f"Failed: {e}")

############################################################################################################################
############################################################################################################################

def monitor_csv_file():
    try:
        print('Hello')

    except Exception as e:
        logging.error(traceback.format_exc())

############################################################################################################################
############################################################################################################################

def start_monitoring(files):
    try:
        threads = []

        for file in files:
            # Extract file path
            file_path = file['path']
            file_type = file['type']

            # Determine the which function to use and its arguments based on file type
            if file_type == 'log':
                thread = threading.Thread(target=monitor_log_file, args=(file_path,))
            elif file_type == 'csv':
                thread = threading.Thread(target=monitor_csv_file, args=(file_path,))
            else:
                print(f"Unsupported file type for {file_path}")
                continue  # Skip unsupported file types
            
            threads.append(thread)
            thread.start()
    
    except Exception:
        logging.error(traceback.format_exc())

############################################################################################################################
############################################################################################################################

def convert_logfile_data_to_json(log_file_path):
    # Open the log file
    with open(log_file_path, 'r') as log_file:
        # Read all lines from the file
        lines = log_file.readlines()

    # Skip the header and process each line
    log_data = []
    for line in lines[1:]:
        parts = line.strip().split(',')
        if log_file_path == "C:\\Users\\User\\AppData\\Local\\Firaxis Games\\Sid Meier\'s Civilization VI\\Logs\\AStar_GC.log":
            log_entry = {
                "GameTurn": parts[0].strip(),
                "Player": parts[1].strip(),
                "Unit": parts[2].strip(),
                "FromX": int(parts[3].strip()),
                "FromY": int(parts[4].strip()),
                "ToX": int(parts[5].strip()),
                "ToY": int(parts[6].strip()),
                "Info": int(parts[7].strip()),
                "Checksum": parts[8].strip()
            }

        log_data.append(log_entry)

    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(log_data)

    return json_data

############################################################################################################################
############################################################################################################################

def convert_new_logline_to_json(log_file_path, line):
    with open(log_file_path, "r") as logfile: 
        log_data = []
        parts = line.strip().split(',')
        if log_file_path == "C:\\Users\\User\\AppData\\Local\\Firaxis Games\\Sid Meier\'s Civilization VI\\Logs\\AStar_GC.log":
            log_entry = {
                "GameTurn": parts[0].strip(),
                "Player": parts[1].strip(),
                "Unit": parts[2].strip(),
                "FromX": int(parts[3].strip()),
                "FromY": int(parts[4].strip()),
                "ToX": int(parts[5].strip()),
                "ToY": int(parts[6].strip()),
                "Info": int(parts[7].strip()),
                "Checksum": parts[8].strip()
            }
        log_data.append(log_entry)
    
    # Convert the list of dictionaries to JSON format
    json_data = json.dumps(log_data)

    return json_data


############################################################################################################################
############################################################################################################################

def send_it(table_name, json_data):
    dce_endpoint = "https://civ6-dce-5uqg.australiaeast-1.ingest.monitor.azure.com" # ingestion endpoint of the Data Collection Endpoint object
    dcr_immutableid = "dcr-2434728ef0d641668ce479cfbad78e61" # immutableId property of the Data Collection Rule
    stream_name = table_name #name of the stream in the DCR that represents the destination table

    credential = DefaultAzureCredential()
    client = LogsIngestionClient(endpoint=dce_endpoint, credential=credential, logging_enable=True)

    body = [json.loads(json_data)]

    try:
        client.upload(rule_id=dcr_immutableid, stream_name=stream_name, logs=body)
    except HttpResponseError as e:
        print(f"Upload failed: {e}")

############################################################################################################################
############################################################################################################################

start_monitoring(files)