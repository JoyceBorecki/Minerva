import sys
import psutil
import os
from compressor_lzw import compactar_arquivo, descompactar_arquivo, calcular_hash

BASE_DIR = "arquivos_teste"
ENTRADA_DIR = os.path.join(BASE_DIR, "entrada")
COMPACTADOS_DIR = os.path.join(BASE_DIR, "compactados")
DESCOMPACTADOS_DIR = os.path.join(BASE_DIR, "descompactados")

def main():
    if len(sys.argv) != 3:
        print("Uso:")
        print("  python compressor_lzw/interface_cli.py compactar <arquivo.txt>")
        print("  python compressor_lzw/interface_cli.py descompactar <arquivo.lzw>")
        return

    comando, nome_arquivo = sys.argv[1], sys.argv[2]
    processo = psutil.Process()

    try:
        if comando == "compactar":
            caminho_entrada = os.path.join(ENTRADA_DIR, nome_arquivo)
            caminho_saida = os.path.join(COMPACTADOS_DIR, nome_arquivo.replace(".txt", ".lzw"))
            compactar_arquivo(caminho_entrada, caminho_saida)

        elif comando == "descompactar":
            caminho_entrada = os.path.join(COMPACTADOS_DIR, nome_arquivo)
            caminho_saida = os.path.join(DESCOMPACTADOS_DIR, nome_arquivo.replace(".lzw", "_descompactado.txt"))
            descompactar_arquivo(caminho_entrada, caminho_saida)

            original_path = os.path.join(ENTRADA_DIR, nome_arquivo.replace(".lzw", ".txt"))
            if os.path.exists(original_path):
                hash_original = calcular_hash(original_path)
                hash_resultado = calcular_hash(caminho_saida)
                if hash_original == hash_resultado:
                    print("Arquivo descompactado é idêntico ao original.")
                else:
                    print("Arquivo descompactado é diferente do original!")

        else:
            print("Comando inválido. Use: compactar | descompactar")
            return

        memoria_mb = processo.memory_info().rss / (1024 * 1024)
        print(f"Memória usada: {memoria_mb:.2f} MB")

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
