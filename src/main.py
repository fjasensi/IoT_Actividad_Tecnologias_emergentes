import os
from dotenv import load_dotenv

load_dotenv()

# Get environ variables
CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID")
READ_API_KEY = os.getenv("THINGSPEAK_READ_API_KEY")
WRITE_API_KEY = os.getenv("THINGSPEAK_WRITE_API_KEY")

if not all([CHANNEL_ID, READ_API_KEY, WRITE_API_KEY]):
    print("Error: Environ variables missing.")
    print("Please, setup all environ variables in .env file")
    exit(1)

def main():
    print(f"Hello World {CHANNEL_ID}")

if __name__ == "__main__":
    main()