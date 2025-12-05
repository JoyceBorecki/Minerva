import sys
import os

from src.compactacao.lzw import compactar_arquivo, descompactar_arquivo, buscar_substring_compactado
from src.busca.kmp import iter_busca_kmp
from src.util.arquivos import calcular_hash
from src.util.memoria import get_memory_usage_mb

BASE_DIR = "data"
ENTRADA_DIR = os.path.join(BASE_DIR, "entrada")
COMPACTADOS_DIR = os.path.join(BASE_DIR, "compactados")
DESCOMPACTADOS_DIR = os.path.join(BASE_DIR, "descompactados")

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python src/cli.py compactar <arquivo.txt>")
        print("  python src/cli.py descompactar <arquivo.lzw>")
        print('  python src/cli.py buscar_simples <arquivo.txt> "<substring>"')
        print('  python src/cli.py buscar_compactado <arquivo.lzw> "<substring>"')
        return

    comando = sys.argv[1]
    nome_arquivo = sys.argv[2]

    try:
        if comando == "compactar":
            caminho_entrada = os.path.join(ENTRADA_DIR, nome_arquivo)
            caminho_saida = os.path.join(COMPACTADOS_DIR, nome_arquivo.replace(".txt", ".lzw"))
            compactar_arquivo(caminho_entrada, caminho_saida)

        elif comando == "descompactar":
            caminho_entrada = os.path.join(COMPACTADOS_DIR, nome_arquivo)
            caminho_saida = os.path.join(DESCOMPACTADOS_DIR, nome_arquivo.replace(".lzw", "_descompactado.txt"))
            descompactar_arquivo(caminho_entrada, caminho_saida)

            original = os.path.join(ENTRADA_DIR, nome_arquivo.replace(".lzw", ".txt"))
            if os.path.exists(original):
                if calcular_hash(original) == calcular_hash(caminho_saida):
                    print("Arquivo descompactado é idêntico ao original.")
                else:
                    print("Arquivo descompactado é diferente do original.")

        elif comando == "buscar_simples":
            if len(sys.argv) < 4:
                print('Uso: python src/cli.py buscar_simples <arquivo.txt> "<substring>"')
                return

            substring = sys.argv[3]
            caminho = nome_arquivo if os.path.isabs(nome_arquivo) else os.path.join(ENTRADA_DIR, nome_arquivo)

            if not os.path.exists(caminho):
                print(f"Arquivo '{nome_arquivo}' não encontrado.")
                return

            offsets = iter_busca_kmp(caminho, substring.encode())
            print(" ".join(map(str, offsets)))
            return

        elif comando == "buscar_compactado":
            if len(sys.argv) < 4:
                print('Uso: python src/cli.py buscar_compactado <arquivo.lzw> "<substring>"')
                return

            substring = sys.argv[3]
            caminho = nome_arquivo if os.path.isabs(nome_arquivo) else os.path.join(COMPACTADOS_DIR, nome_arquivo)

            if not os.path.exists(caminho):
                print(f"Arquivo '{nome_arquivo}' não encontrado.")
                return

            offsets = buscar_substring_compactado(caminho, substring)
            print(" ".join(map(str, offsets)))
            return

        else:
            print("Comando inválido.")
            return

        print(f"Memória usada: {get_memory_usage_mb():.2f} MB")

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
