import subprocess
import requests
import json
import time

# Define the osquery queries and their simplified names as a dictionary
osquery_queries = {
    "SELECT CONCAT(hostname, '-', uuid) AS unique_id FROM system;": "unique_id",
    "SELECT name, version FROM os_version;": "os_version",
    "SELECT name FROM programs WHERE name LIKE '%avast%' OR name LIKE '%antivirus%';": "antivirus_programs",
    "SELECT CASE WHEN protection_status = 0 THEN 'Hard drive not encrypted' ELSE 'Hard drive encrypted' END AS encryption_status FROM bitlocker_info LIMIT 1;": "bitlocker_status",
    "SELECT CASE WHEN name IN ('LastPass', '1Password', 'Bitwarden', 'Dashlane', 'Keeper', 'RoboForm', 'NordPass', 'Enpass', 'Sticky Password', 'Password Safe', 'Myki', 'RememBear') THEN name ELSE 'No password manager in use' END AS password_manager FROM programs WHERE name IN ('LastPass', '1Password', 'Bitwarden', 'Dashlane', 'Keeper', 'RoboForm', 'NordPass', 'Enpass', 'Sticky Password', 'Password Safe', 'Myki', 'RememBear') UNION SELECT 'No password manager in use' AS password_manager WHERE (SELECT COUNT(*) FROM programs WHERE name IN ('LastPass', '1Password', 'Bitwarden', 'Dashlane', 'Keeper', 'RoboForm', 'NordPass', 'Enpass', 'Sticky Password', 'Password Safe', 'Myki', 'RememBear')) = 0;": "password_manager",
    "SELECT username FROM users WHERE directory LIKE 'C:\\Users\\%';": "usernames",
    "SELECT name, data FROM registry WHERE key = 'HKEY_CURRENT_USER\\Control Panel\\Desktop' AND (name = 'ScreenSaveActive' OR name = 'ScreenSaverIsSecure');":"screen Lock",
}

# Define the API endpoint where you want to send the data
endpoint_url = "https://api.vistar.cloud/api/v1/computers/osquery_log_data/"

# Specify the interval (in seconds) between data sends (e.g., every 1 hour)
interval_seconds = 3600  # 1 hour

while True:
    # Initialize an empty dictionary to store the results of all queries
    all_osquery_data = {}

    # Run each osquery query and capture the output
    for query, simplified_name in osquery_queries.items():
        try:
            osquery_output = subprocess.check_output(["C:\\Program Files\\osquery\\osqueryi.exe", "--json", query], shell=True)
            osquery_data = json.loads(osquery_output.decode())
            all_osquery_data[simplified_name] = osquery_data
        except subprocess.CalledProcessError as e:
            print(f"Error running osquery for query '{query}':", e)
        except Exception as e:
            print(f"Error processing query '{query}':", e)

    # Send the combined data to the endpoint using the requests library
    try:
        response = requests.post(endpoint_url, json=all_osquery_data)
        if response.status_code == 201:
            print("Data sent successfully. Status code: 201")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print("Error sending data:", e)



    # Sleep for the specified interval before the next run
    time.sleep(interval_seconds)
