import os
from dotenv import load_dotenv
from thing_speak_manager import ThingSpeakManager

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
    ts_manager = ThingSpeakManager(CHANNEL_ID, READ_API_KEY, WRITE_API_KEY)

    while True:
        print("=" * 50)
        print("GESTOR DE DATOS DE MONITOREO AMBIENTAL - ThingSpeak")
        print("=" * 50)
        print(f"\nCanal configurado: {ts_manager.channel_id}")
        print("\nOpciones:")
        print("1. Ver últimas lecturas")
        print("2. Ver estado del canal")
        print("3. Añadir nueva lectura manualmente")
        print("0. Salir")

        option = input("\nSelecciona una opción: ")

        if option == "0":
            # Exit
            print("\nSaliendo del programa...")
            break
        elif option == "1":
            # Show most recent data
            results = input("Número de lecturas a mostrar (Enter para 10): ")
            results = int(results) if results.isdigit() else 10

            ts_manager.display_data_table(results)

            input("\nPresiona Enter para continuar...")
        else:
            print("\nOpción no válida. Inténtalo de nuevo.")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()