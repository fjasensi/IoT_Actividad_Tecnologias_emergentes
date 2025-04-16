import unittest
import os
from pathlib import Path


class TestConfiguration(unittest.TestCase):
    """Verify ThingSpeak config"""

    def test_env_file_exists(self):
        """Verify if .env file exists"""
        env_file = Path('.env')

        file_exists = env_file.exists()

        if not file_exists:
            print("Please, create .env file with your credentials.")
            print("You can show an example in .env.example")

        self.assertTrue(file_exists, "No configuration file found (.env)")


    def test_env_variables_available(self):
        """Verify if the environ variables are available"""
        if Path('.env').exists():
            from dotenv import load_dotenv
            load_dotenv()

            env_vars = [
                "THINGSPEAK_CHANNEL_ID",
                "THINGSPEAK_READ_API_KEY",
                "THINGSPEAK_WRITE_API_KEY"
            ]

            missing_vars = [var for var in env_vars if not os.getenv(var)]

            if missing_vars:
                print(f"\n⚠️  WARNING: The following environ variables are missing in .env file.")
                for var in missing_vars:
                    print(f"   - {var}")

            self.assertEqual(len(missing_vars), 0, f"Environ variables missing: {', '.join(missing_vars)}")


if __name__ == '__main__':
    unittest.main()