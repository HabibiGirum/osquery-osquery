import subprocess
import json
import os

def get_unique_id():
    try:
        # Check both possible paths for osqueryd.exe
        possible_paths = [
            r'C:\Program Files\osquery\osqueryi.exe',
        ]

        osquery_path = None

        for path in possible_paths:
            if os.path.exists(path):
                osquery_path = path
                break

        if not osquery_path:
            print("osqueryd.exe not found in the specified paths.")
            return None

        # Run the osqueryd command to retrieve unique_id from system_info
        cmd = [osquery_path, "--config_path", "C:/Program Files/osquery/osqueryi.exe", "--json", "SELECT CONCAT(hostname, '-', uuid) AS unique_id FROM system_info"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)

        # Parse the JSON output
        output = result.stdout.strip()
        data = json.loads(output)
        unique_id = data[0]['unique_id']

        # Replace hyphens with underscores
        modified_unique_id = unique_id.replace('-', '_')

        return modified_unique_id
    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main":
    unique_id = get_unique_id()
    if unique_id:
        print("Modified Unique ID:", unique_id)

        # Send modified unique ID to the specified URL
        redirect_url = f"https://app.vistar.cloud/redirects/mdm?computer={unique_id}"
        print("Redirect URL:", redirect_url)

        # Open Chrome without displaying the console window
        chrome_driver_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        subprocess.Popen([chrome_driver_path, redirect_url], creationflags=subprocess.CREATE_NO_WINDOW)

        try:
            # Wait for the browser window to close
            while True:
                pass  # You don't need to check the driver here since it's not used
        except Exception as e:
            print("An error occurred:", e)
        finally:
            print("Exiting the script.")
