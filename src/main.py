import os
import json
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
        print("3. Ver datos de un campo")
        print("4. Añadir nueva lectura manualmente")
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
        elif option == "2":
            # Get status of the channel
            status = ts_manager.read_channel_status()

            if status:
                print("\nEstado del canal:")
                print(json.dumps(status, indent=2))

            input("\nPresiona Enter para continuar...")
        elif option == "3":
            # Read a specific field from the channel
            print("\nSelecciona el campo para ver sus datos:")

            for i, field_name in enumerate(ts_manager.field_names.values(), 1):
                print(f"{i}. {field_name}")

            field_option = input("\nSelecciona una opción (1-5): ")
            if field_option.isdigit() and 1 <= int(field_option) <= 5:
                results = input("Número de lecturas a mostrar (Enter para 10): ")
                results = int(results) if results.isdigit() else 10

                # Read and display data for the selected field
                ts_manager.display_field_data(int(field_option), results)

            input("\nPresiona Enter para continuar...")
        elif option == "4":
            # Add a new record
            print("\nIntroduce los valores para la nueva lectura:")
            new_data = {}

            for field_key, field_name in ts_manager.field_names.items():
                while True:
                    value = input(f"{field_name}: ")
                    try:
                        new_data[field_key] = float(value)
                        break
                    except ValueError:
                        print("Error: Introduce un valor numérico válido.")

            # Confirmation before send
            print("\nDatos a enviar:")

            for field_key, value in new_data.items():
                print(f"{ts_manager.field_names[field_key]}: {value}")

            confirm = input("\n¿Confirmar envío? (s/n): ")

            if confirm.lower() == 's':
                status_code = ts_manager.write_channel_data(new_data)
                if status_code == 200:
                    print("Datos enviados correctamente.")
                else:
                    print(f"Error al enviar datos. Código de estado: {status_code}")
            else:
                print("Envío cancelado.")

            input("\nPresiona Enter para continuar...")
        else:
            print("\nOpción no válida. Inténtalo de nuevo.")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()