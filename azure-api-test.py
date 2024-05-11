# information needed to send data to the DCR endpoint
dce_endpoint = "https://civ6-dce-5uqg.australiaeast-1.ingest.monitor.azure.com" # ingestion endpoint of the Data Collection Endpoint object
dcr_immutableid = "dcr-2434728ef0d641668ce479cfbad78e61" # immutableId property of the Data Collection Rule
stream_name = "Custom-testtable_CL" #name of the stream in the DCR that represents the destination table

# Import required modules
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.ingestion import LogsIngestionClient
from azure.core.exceptions import HttpResponseError

credential = DefaultAzureCredential()
client = LogsIngestionClient(endpoint=dce_endpoint, credential=credential, logging_enable=True)

body = [
{
    "ABC":"XYZ",
    "TimeGenerated":"2024-05-11T01:41:45.582Z"
}
    ]

try:
    client.upload(rule_id=dcr_immutableid, stream_name=stream_name, logs=body)
except HttpResponseError as e:
    print(f"Upload failed: {e}")