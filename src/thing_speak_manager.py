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