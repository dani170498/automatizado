import wget
import gzip
import shutil
import os
import subprocess

class NistDataDownloader:
    def __init__(self, url, compressed_file, decompressed_file, delete_compressed=True):
        self.url = url
        self.compressed_file = compressed_file
        self.decompressed_file = decompressed_file
        self.delete_compressed = delete_compressed

    def descargar_archivo(self):
        print("Descargando archivo comprimido...")
        wget.download(self.url, self.compressed_file)
        print("\nDescarga completada.")

    def descomprimir_archivo(self):
        print("Descomprimiendo archivo...")
        with gzip.open(self.compressed_file, 'rb') as f_in, open(self.decompressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print("Descompresión completada.")

    def eliminar_archivo_comprimido(self):
        if self.delete_compressed:
            os.remove(self.compressed_file)
            print("Archivo comprimido eliminado.")

    def filtrar_y_redirigir(self):
        comando = (
            f"cat {self.decompressed_file} | "
            "grep 'wordpress' | "
            "grep -v 'reference' | "
            "grep -v '<cpe-item name=\"' | "
            "grep -Eo 'name=.*' | "
            "grep -Eo '\".*\"' | "
            "sed 's/\"//g' >> /home/daniel/automatizado/archivos/cpe.txt"
        )

        print("Ejecutando proceso de filtrado y redirección...")
        subprocess.run(comando, shell=True)
        print("Proceso completado.")
        os.remove(self.decompressed_file)
        print("Archivo XML eliminado.")

def descargar_descomprimir_filtrar():
    url = "https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz"
    compressed_file = "/home/daniel/automatizado/archivos/official-cpe-dictionary_v2.3.xml.gz"
    decompressed_file = "/home/daniel/automatizado/archivos/official-cpe-dictionary_v2.3.xml"

    downloader = NistDataDownloader(url, compressed_file, decompressed_file)
    downloader.descargar_archivo()
    downloader.descomprimir_archivo()
    downloader.eliminar_archivo_comprimido()
    downloader.filtrar_y_redirigir()

if __name__ == "__main__":
    descargar_descomprimir_filtrar()
