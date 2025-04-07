import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === Config ===
username = "admin"
password = "EWeBBqOF8LwcHDQI"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
}

# === Session ===
session = requests.Session()
session.auth = HTTPBasicAuth(username, password)

# === Create Definition ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
job_name = f"job_{timestamp}"

# definition_payload = {
#     "migration_job_name": job_name,
#     "source_host": "206.12.93.212",
#     "target_host": "206.12.101.10",
#     "source_user": "db2inst1",
#     "target_user": "db2inst1",
#     "source_password": "M0untainn",
#     "target_password": "password",
#     "source_database": "testdb",
#     "target_database": "testdb",
#     "source_port": 50000,
#     "target_port": 50000,
#     "source_ssl": False,
#     "target_ssl": False,
#     "binary": True,
#     "compression": "LZ4",
#     "grants": "OBJECT",
#     "hpu_mode": False,
#     "whole_db": False,
#     "hpu_path": "",
#     "backup_path": "",
#     "hidden_columns": False,
#     "maintenance_mode": False,
#     "parallel_data_streams": 1,
#     "audit_policies": [],
#     "roles": [],
#     "security_labels": [],
#     "security_label_components": [],
#     "security_policies": [],
#     "histogram_templates": [],
#     "service_classes": [],
#     "bufferpools": [],
#     "tablespaces": [],
#     "tables": ["DB2INST1.TEST"],
#     "comments": [],
#     "indexes": [],
#     "sequences": [],
#     "triggers": [],
#     "views": [],
#     "aliases": [],
#     "procedures": [],
#     "functions": [],
#     "constraints": [],
#     "global_variables": [],
#     "modules": [],
#     "types": []
# }

# Create definition
# definition_url = "https://localhost:14080/migration/definitions/"
# response = session.post(definition_url, headers=headers, json=definition_payload, verify=False)

# print("Create Definition Status:", response.status_code)
# definition_response = response.json()
# print("Create Response:", definition_response)

# # === Extract definition_id and trigger migration ===
# definition_id = definition_response.get("definition_id")

# if definition_id:
#     run_url = f"https://localhost:14080/migration/migration_service_data_transfer/run/{definition_id}"
#     run_response = session.post(run_url, headers=headers, verify=False)
    
#     print("Run Migration Status:", run_response.status_code)
#     try:
#         print("Run Response:", run_response.json())
#     except Exception:
#         print("Raw Run Response:", run_response.text)
# else:
#     print("No definition_id returned. Cannot trigger migration.")
        # Ensure job_id is available
job_id = "8128020138074dcd9c6ae02a636155d3"     
if job_id:
    # Build the URL for fetching logs
    logs_url = f"https://localhost:14080/migration/migration_service_data_transfer/jobs"
    
    # Send the GET request to fetch logs
    logs_response = session.get(logs_url)

    # Print the status code of the logs request
    #print("Fetching Logs Response:", logs_response)
    
    logs = logs_response.get('log_content')

    print(logs)