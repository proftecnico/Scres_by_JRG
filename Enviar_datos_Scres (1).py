import serial
import time
import os
import sys

# Encabezado
header = """
███████╗ ██████╗██████╗ ███████╗███████╗  
██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝
███████╗██║     ██████╔╝█████╗  ███████╗
╚════██║██║     ██╔══██╗██╔══╝  ╚════██║
███████║╚██████╗██║  ██║███████╗███████║
╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝    By Jorge Garavagno     
                                            
"""
print(header)

# Configura el puerto serie
try:
    ser = serial.Serial('COM6', 9600, timeout=1)  # Reemplaza 'COM#' con el puerto correcto
    print("Conexión establecida con el puerto serial.")
except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
    ser = None

# Función para mostrar la barra de progreso
def mostrar_barra_progreso(porcentaje, longitud=30):
    progreso = int(porcentaje / 100 * longitud)
    barra = '█' * progreso + '░' * (longitud - progreso)
    sys.stdout.write(f"\r{barra} {porcentaje:.2f}%")
    sys.stdout.flush()

# Verifica que el puerto se haya abierto correctamente
if ser and ser.is_open:
    file_path = r'C:\SCRES\concatenado.scres'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            total_lines = len(lines)

            for i, line in enumerate(lines):
                line = line.strip()  # Elimina espacios en blanco y saltos de línea al principio y al final
                if line:  # Verifica que la línea no esté vacía
                    ser.write(line.encode())  # Envía la línea al ESP8266
                    time.sleep(2)  # Ajusta el tiempo según la necesidad de procesamiento del Arduino

                    # Calcula el porcentaje de avance y muestra la barra de progreso
                    progress = (i + 1) / total_lines * 100
                    mostrar_barra_progreso(progress)

                    # Lee la respuesta del Arduino si es necesario
                    if ser.in_waiting > 0:
                        response = ser.readline().decode().strip()
                        print(f"\nArduino responde: {response}")

        print("\nEnvío de datos completado.")
        
        # Cierra el puerto serial
        ser.close()

        # Elimina el archivo después de enviar los datos
        os.remove(file_path)
        print("Archivo eliminado.")

    except FileNotFoundError:
        print(f"Error: El archivo en {file_path} no se encontró.")
    except Exception as e:
        print(f"Error al enviar datos: {e}")

else:
    print("No se pudo establecer la conexión serial.")
