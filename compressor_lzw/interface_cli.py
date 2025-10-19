import sys
import psutil
from compressor_lzw import compactar_arquivo, descompactar_arquivo

def main():
    if len(sys.argv) != 4:
        print("Uso: python compressor_lzw/interface_cli.py <comando> <entrada> <saida>")
        print("Comandos: compactar | descompactar")
        return

    comando, entrada, saida = sys.argv[1], sys.argv[2], sys.argv[3]
    processo = psutil.Process()

    try:
        if comando == "compactar":
            compactar_arquivo(entrada, saida)
        elif comando == "descompactar":
            descompactar_arquivo(entrada, saida)
        else:
            print("Comando inválido. Use: compactar | descompactar")
            return

        memoria_mb = processo.memory_info().rss / (1024 * 1024)
        print(f"Memória usada: {memoria_mb:.2f} MB")

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
