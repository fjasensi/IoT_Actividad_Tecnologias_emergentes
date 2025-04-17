import requests
from tabulate import tabulate


class ThingSpeakManager:
    def __init__(self, channel_id=None, read_api_key=None, write_api_key=None):
        self.channel_id = channel_id
        self.read_api_key = read_api_key
        self.write_api_key = write_api_key
        self.base_url = "https://api.thingspeak.com"
        self.configured = all([channel_id, read_api_key, write_api_key])

        self.field_names = {
            "field1": "CO2 (ppm)",
            "field2": "Ruido (dB)",
            "field3": "Luminosidad (lux)",
            "field4": "Presión (hPa)",
            "field5": "Viento (km/h)"
        }

    def check_configuration(self):
        if not self.configured:
            return False

        return True

    def read_channel_data(self, results=10):
        """
        Read the most recent data from the channel

        Args:
            results (int): Number of entries to retrieve

        Returns:
            dict: Data retrieved from the channel
        """
        if not self.check_configuration():
            return None

        endpoint = f"{self.base_url}/channels/{self.channel_id}/feeds.json"
        params = {
            "api_key": self.read_api_key,
            "results": results
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error reading data from chanel: {e}")
            return None

    def read_channel_status(self):
        """
        Reads the current status of the channel

        Returns:
            dict: Data retrieved from the status of the channel
        """
        if not self.check_configuration():
            return None

        endpoint = f"{self.base_url}/channels/{self.channel_id}/status.json"
        params = {
            "api_key": self.read_api_key
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error reading the status of the channel: {e}")
            return None

    def write_channel_data(self, field_values):
        """
        Write new data in the channel

        Args:
            field_values (dict): Values for each field (ex: {"field1": 450.23})

        Returns:
            int: HTTP status code from the response
        """
        if not self.check_configuration():
            return None

        endpoint = f"{self.base_url}/update"
        params = {
            "api_key": self.write_api_key,
            **field_values
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error writing data in the channel: {e}")
            return None

    def display_data_table(self, results=10):
        """
        Shows the most recent data from the channel in table format

        Args:
            results (int): Number of entries to retrieve
        """
        if not self.check_configuration():
            return

        data = self.read_channel_data(results)
        if not data or "feeds" not in data:
            print("No data could be retrieved from the channel")
            return

        feeds = data["feeds"]

        table_data = []
        headers = ["Fecha/Hora"] + list(self.field_names.values())

        for feed in feeds:
            row = [feed.get("created_at")]
            for field_key in self.field_names.keys():
                row.append(feed.get(field_key, "N/A"))
            table_data.append(row)

        # Show table
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def read_channel_field(self, field_number, results=10):
        """
        Reads data from a specific channel field

        Args:
            field_number (int): Field number to read (1-5)
            results (int, optional): Number of entries to retrieve. Defaults to 10.

        Returns:
            dict: Data from the specific field
        """
        if not self.check_configuration():
            return None

        field_key = f"field{field_number}"

        if field_key not in self.field_names:
            print(f"Error: Field {field_number} is not valid.")
            return None

        endpoint = f"{self.base_url}/channels/{self.channel_id}/fields/{field_number}.json"

        params = {
            "api_key": self.read_api_key,
            "results": results
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()  # Raises an exception for HTTP errors
            data = response.json()

            # Print summary information
            if "feeds" in data and data["feeds"]:
                num_entries = len(data["feeds"])
                field_name = self.field_names[field_key]
                print(f"Retrieved {num_entries} records for {field_name}")

            return data
        except requests.exceptions.RequestException as e:
            print(f"Error reading data from field {field_number}: {e}")
            return None

    def display_field_data(self, field_number, results=10):
        """
        Displays data from a specific field in table format

        Args:
            field_number (int): Field number to display (1-5)
            results (int, optional): Number of entries to display. Defaults to 10.
        """
        if not self.check_configuration():
            return

        field_key = f"field{field_number}"

        if field_key not in self.field_names:
            print(f"Error: Field {field_number} is not valid.")
            return

        data = self.read_channel_field(field_number, results)

        if not data or "feeds" not in data:
            print(f"Could not retrieve data from field {field_number}.")
            return

        feeds = data["feeds"]

        # Prepare data for the table
        table_data = []
        headers = ["Timestamp", self.field_names[field_key]]

        for feed in feeds:
            created_at = feed.get("created_at", "N/A")
            field_value = feed.get(field_key, "N/A")
            table_data.append([created_at, field_value])

        # Display table
        print(f"\nData for field: {self.field_names[field_key]}")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))