import os

def eliminar_archivo(ruta):
    try:
        os.remove(ruta)
        print(f"Archivo en {ruta} eliminado con éxito.")
    except FileNotFoundError:
        print(f"El archivo en {ruta} no existe.")
    except Exception as e:
        print(f"Error al eliminar el archivo en {ruta}: {str(e)}")

def main():
    rutas_a_eliminar = [
        '/home/daniel/automatizado/diccionario/diccionario.json',
        '/home/daniel/automatizado/diccionario/elemento.json',
        '/home/daniel/automatizado/diccionario/evaluar.json',
        '/home/daniel/automatizado/archivos/cpe.txt'
    ]

    for ruta in rutas_a_eliminar:
        eliminar_archivo(ruta)

if __name__ == "__main__":
    main()
