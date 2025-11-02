import sys
import os
from src.compactacao.lzw import compactar_arquivo, descompactar_arquivo
from src.busca.kmp import buscar_substring, iter_busca_kmp
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
        return

    comando, nome_arquivo = sys.argv[1], sys.argv[2]

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

        elif comando == "buscar_simples":
            if len(sys.argv) < 4:
                print('Uso: python src/cli.py buscar_simples <arquivo.txt> "<substring>"')
                return

            substring = sys.argv[3]

            if os.path.isabs(nome_arquivo):
                caminho_entrada = nome_arquivo
            else:
                caminho_entrada = os.path.join(ENTRADA_DIR, nome_arquivo)

            if not os.path.exists(caminho_entrada):
                print(f"Arquivo '{nome_arquivo}' não encontrado em '{ENTRADA_DIR}'.")
                return

            padrao_bytes = substring.encode("utf-8")
            offsets_iter = iter_busca_kmp(caminho_entrada, padrao_bytes, tamanho_bloco=8 << 20)
            print(" ".join(map(str, offsets_iter)))
            return

        else:
            print("Comando inválido. Use: compactar | descompactar | buscar_simples")
            return

        memoria_mb = get_memory_usage_mb()
        print(f"Memória usada: {memoria_mb:.2f} MB")

    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
